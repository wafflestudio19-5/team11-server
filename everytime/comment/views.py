from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q
from django.db import transaction

from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action, parser_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from user.models import User
from board.models import Board
from article.models import Article, UserArticle
from comment.models import Comment, UserComment

from .serializers import CommentCreateSerializer, CommentSerializer, UserCommentSerializer

from common.fcm_notification import send_push

import logging
logger = logging.getLogger('django')

class CommentViewSet(viewsets.GenericViewSet):
    serializer_class = CommentCreateSerializer

    def check_board_article(self, board_id, article_id):
        if not (board := Board.objects.get_or_none(id=board_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_board_id", "detail" : "게시판이 존재하지 않습니다."})
        if not (article := Article.objects.get_or_none(id=article_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_article_id", "detail" : "게시글이 존재하지 않습니다."})
        if article.board != board:
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_match", "detail" : "해당 게시판의 게시글이 아닙니다."})

    #POST /board/{board_id}/article/{article_id}/comment/
    def create(self, request, board_id, article_id):
        self.check_board_article(board_id, article_id)

        data = request.data.copy()
        serializer = CommentCreateSerializer(data=data, context={'request': request, 'article_id': article_id})
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        if comment.is_subcomment == True:
            # parent 댓글 구독한 사람에게 알림 전송
            try:
                uc = UserComment.objects.filter(comment=comment.parent, subscribe=True).exclude(user=request.user)
                fcm_tokens = User.objects.filter(user_comment__in=uc, fcm_token__isnull=False).values("fcm_token")
                for fcm_token in fcm_tokens:
                    logger.debug(fcm_token)
                    send_push("new_subcomment", comment, fcm_token['fcm_token'])
            except Exception as e:
                logger.debug(e)
        else:
            user_comment = UserComment.objects.create(comment=comment, user=request.user, subscribe=True)
            # 게시글 구독한 사람에게 알림 전송
            try:
                ua = UserArticle.objects.filter(article=article_id, subscribe=True).exclude(user=request.user)
                fcm_tokens = User.objects.filter(user_article__in=ua, fcm_token__isnull=False).values("fcm_token")
                for fcm_token in fcm_tokens:
                    logger.debug(fcm_token)
                    send_push("new_comment", comment, fcm_token['fcm_token'])
            except Exception as e:
                logger.debug(e)
        
        user_article = UserArticle.objects.get_or_none(article_id=article_id, user=request.user)
        if user_article == None:
            user_article = UserArticle.objects.create(article_id=article_id, user=request.user)
        if comment.is_anonymous ==True and user_article.nickname_code == None:
            last_nickname_code = UserArticle.objects.filter(article=article_id).order_by("nickname_code").last().nickname_code
            if bool(last_nickname_code) == False:
                nickname_code = 1
            else:
                nickname_code = last_nickname_code + 1
            user_article.nickname_code = nickname_code
            user_article.save()

        return Response(status=status.HTTP_200_OK, data={"success" : True, "comment_id" : comment.id})

    #DELETE /board/{board_id}/article/{article_id}/comment/{comment_id}
    def destroy(self, request, board_id, article_id, pk):
        self.check_board_article(board_id, article_id)
        article = Article.objects.get_or_none(id=article_id)

        if not (comment := Comment.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_comment_id", "detail" : "댓글이 존재하지 않습니다."})
        comment = Comment.objects.get(id = pk)
        if comment.article != article:
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_match", "detail" : "해당 게시글의 댓글이 아닙니다."})

        has_subcomments = lambda c: Comment.objects.filter(Q(parent=c)&~Q(id=c.id)).exists()
        #has_subcomments = Comment.objects.filter(Q(parent=comment)&~Q(id=comment.id)).exists()
        
        with transaction.atomic():
            # 1. 대댓글 - 바로삭제
            if comment.is_subcomment:
                print("대댓글")
                parent = comment.parent
                comment.delete()
                # 원댓글이 "삭제 상태 & subcomment가 없음" -> 삭제
                if parent.is_active == False and not has_subcomments(parent) :
                    parent.delete()

            # 2. 원댓글 with no 대댓글 - 바로 삭제
            elif not has_subcomments(comment):
                print("원댓글 with no 대댓글")
                comment.delete()

            # 3. 원댓글 with 대댓글 - is_active=False, writer=NULL, text->삭제된 댓글입니다.
            elif has_subcomments(comment):
                print("원댓글 with 대댓글")
                comment.is_active = False
                comment.commenter = None
                comment.text = "삭제된 댓글입니다."
                comment.save()


        return Response(status=status.HTTP_200_OK, data={"success" : True})
    
    def list(self, request, board_id, article_id):
        self.check_board_article(board_id, article_id)
        article = Article.objects.get_or_none(id=article_id)

        comments = Comment.objects.filter(article = article)
        
        return Response(status=status.HTTP_200_OK, data={"comments" : CommentSerializer(comments, context = {'request' : request}, many=True).data})

class UserCommentView(viewsets.GenericViewSet):
    serializer_class = UserCommentSerializer

    def create(self, request, comment_id):
        comment = Comment.objects.get_or_none(id=comment_id)

        if not comment:
            return Response(status=status.HTTP_404_NOT_FOUND, 
                            data={ "error":"wrong_comment_id", "detail" : "댓글이 존재하지 않습니다."})

        if not (user_comment := UserComment.objects.get_or_none(user = request.user, comment = comment)):
            serializer = self.get_serializer(data={})
            serializer.is_valid(raise_exception=True)
            user_comment = serializer.save()
        else:
            user_comment = UserComment.objects.get(user = request.user, comment = comment)
            serializer = self.get_serializer(user_comment, data={}, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.update(user_comment, serializer.validated_data)

        return self.get_response(comment, user_comment)

class UserCommentLikeView(UserCommentView):
    def get_response(self, comment, user_comment):
        return Response(status=status.HTTP_200_OK,
                        data={
                            "like": UserComment.objects.filter(comment = comment, like = True).count(),
                            "detail": "이 댓글을 공감하였습니다."
                            }
                        )

class UserCommentSubscribeView(UserCommentView):
    def get_response(self, comment, user_comment):
        return Response(status=status.HTTP_200_OK,
                        data={
                            "subscribe": user_comment.subscribe,
                            "detail": "대댓글 알림을 켰습니다." if user_comment.subscribe else "대댓글 알림을 껐습니다."
                            }
                        )