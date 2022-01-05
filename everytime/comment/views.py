from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q

from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action, parser_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from board.models import Board
from article.models import Article
from comment.models import Comment, UserComment

from .serializers import CommentCreateSerializer, CommentSerializer, UserCommentSerializer

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

        #serializer = CommentSerializer(comment) 
        # 1. 원댓글 with no 대댓글
        # 바로 삭제
        #has_subcomments = lambda c: x * x
        has_subcomments = Comment.objects.filter(Q(parent=comment)&~Q(id=comment.id)).exists()
         # 1. 대댓글 - 바로삭제
        if comment.is_subcomment:
            print("대댓글")
            # 원댓글이 삭제 상태일 시, 
            #if comment.parent.is_active == False and : 

        # 2. 원댓글 with no 대댓글 - 바로 삭제
        elif has_subcomments:
            print("원댓글 with no 대댓글")
        # 3. 원댓글 with 대댓글 - writer=NULL text->삭제된 댓글입니다.
        elif not has_subcomments:
            print("원댓글 with 대댓글")

        
        # text = 삭제된 댓글입니다.

        # 3. 대댓글 
        # 바로 삭제

        return Response(status=status.HTTP_200_OK, data={"success" : True})
    
    def list(self, request, board_id, article_id):
        self.check_board_article(board_id, article_id)
        article = Article.objects.get_or_none(id=article_id)

        comments = Comment.objects.filter(article = article)
        
        return Response(status=status.HTTP_200_OK, data={"comments" : CommentSerializer(comments, context = {'request' : request}, many=True).data})

class UserCommentLikeView(viewsets.GenericViewSet):
    serializer_class = UserCommentSerializer
    permission_classes = (permissions.AllowAny,)

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

        return Response(status=status.HTTP_200_OK,
                        data={
                            "like": UserComment.objects.filter(comment = comment, like = True).count(),
                            "detail": "이 글을 공감하였습니다."
                            }
                        )