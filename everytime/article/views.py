from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.db.models import Q

from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from operator import itemgetter, attrgetter, methodcaller
from django.db.models.query import QuerySet
from datetime import datetime, timedelta
from .serializers import *
from university.models import University
from board.models import Board
#from .models import Article
import requests

import logging
logger = logging.getLogger('django')

# Create your views here.

class ArticleWholeViewSet(viewsets.GenericViewSet):
    serializer_class = ArticleCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request):
        queryset = self.get_queryset().order_by('-id')

        # # 검색 기능
        # search = self.request.query_params.get('search', None)
        # queryset = self.get_queryset_search(search, queryset)

        # # Hot 게시물, Best 게시물
        # interest = self.request.query_params.get('interest', None)
        # queryset = self.get_queryset_interest(interest, queryset)

        search = request.query_params.get('search', None)

        if not search or search == "":
            return Response(status=status.HTTP_400_BAD_REQUEST, data="put search keyword")

        # 검색 기능
        if search:
            queryset = self.get_queryset_search(search, queryset)
        
        return self.paginate(request, queryset)

    def paginate(self, request, queryset):
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = ArticleSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data) 
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")
    
    def get_queryset(self):
        queryset = Article.objects.all()
        return queryset

    def get_queryset_search(self, search, queryset):
        if search == "":
            return []
        if search:
            q = Q()
            #return queryset.filter(q)
            keywords = set(search.split(' '))
            for k in keywords:
               q &= Q(title__icontains=k)|Q(text__icontains=k)
            queryset = queryset.filter(q)
        return queryset.distinct()
   
class ArticleViewSet(viewsets.GenericViewSet):
    serializer_class = ArticleCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
   
    #POST /board/{board_id}/article/
    def create(self, request, board_id):
        
        if not (board := Board.objects.get_or_none(id=board_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_board_id", "detail" : "게시판이 존재하지 않습니다."})

        data = request.data.copy()
        data['board'] = board_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()

        nickname_code = 0 if article.is_anonymous == True else None
        user_article = UserArticle.objects.create(article=article, user=request.user, subscribe=True, nickname_code=nickname_code)

        return Response(status=status.HTTP_200_OK, data={"success" : True, "article_id" : article.id})


    #GET /board/{board_id}/article/{pk}/
    def retrieve(self, request, board_id, pk=None):
        if not (board := Board.objects.get_or_none(id=board_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_board_id", "detail" : "게시판이 존재하지 않습니다."})
        if not (article := Article.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_article_id", "detail" : "게시글이 존재하지 않습니다."})
        
        board = Board.objects.get(id=board_id)
        article = Article.objects.get(id = pk)

        if article.board != board:
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_match", "detail" : "해당 게시판의 게시글이 아닙니다."})

        return Response(status=status.HTTP_200_OK, 
                        data=ArticleWithCommentSerializer(article, context={'request': request}).data)

    #DELETE /board/{board_id}/article/{pk}/
    def destroy(self, request, board_id, pk=None):
        if not (board := Board.objects.get_or_none(id=board_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_board_id", "detail" : "게시판이 존재하지 않습니다."})
        if not (article := Article.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_article_id", "detail" : "게시글이 존재하지 않습니다."})
        
        board = Board.objects.get(id=board_id)
        article = Article.objects.get(id = pk)

        if article.board != board:
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_match", "detail" : "해당 게시판의 게시글이 아닙니다."})

        if article.is_question and Comment.objects.filter(Q(article=article) & ~Q(article=article, commenter=request.user)):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error": "wrong_match", "detail": "댓글이 달린 질문글은 삭제가 불가능합니다. "})
        
        article.delete()

        return Response(status=status.HTTP_200_OK, data={"success" : True})

    #GET /board/{board_id}/article/?offset=[offset]&?limit=[limit]
    def list(self, request, board_id):
        if not (board := Board.objects.get_or_none(id=board_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_board_id", "detail" : "게시판이 존재하지 않습니다."})

        queryset = self.get_queryset().filter(board_id=board_id).order_by('-id')

        # # 검색 기능
        # search = self.request.query_params.get('search', None)
        # queryset = self.get_queryset_search(search, queryset)

        # # Hot 게시물, Best 게시물
        # interest = self.request.query_params.get('interest', None)
        # queryset = self.get_queryset_interest(interest, queryset)

        search = self.request.query_params.get('search', None)
        interest = self.request.query_params.get('interest', None)

        # 검색 기능
        if search:
            queryset = self.get_queryset_search(search, queryset)
        # Hot 게시물, Best 게시물
        elif interest:
            queryset = self.get_queryset_interest(interest, queryset)
        elif interest and search:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail" : "wrong query parameter"})
        
        return self.paginate(request, queryset)

    def paginate(self, request, queryset):
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = ArticleSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data) 
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")

    def get_queryset(self):
        queryset = Article.objects.all()
        return queryset

    def get_queryset_search(self, search, queryset):
        if search == "":
            return []
        if search:
            q = Q()
            #return queryset.filter(q)
            keywords = set(search.split(' '))
            for k in keywords:
               q &= Q(title__icontains=k)|Q(text__icontains=k)
            queryset = queryset.filter(q)
        return queryset.distinct()
            
        # if search:
        #     queryset_, queryset = queryset, []
        #     search = set(search.split(' '))
        #     for article in queryset_:
        #         article_words = set((article.title+" "+article.text).split(' '))
        #         if search.issubset(article_words):
        #             queryset.append(article)
        # return queryset

    def get_queryset_interest(self, interest, queryset):
        if interest == 'question':
            queryset_, queryset = queryset, []
            for article in queryset_:
                if article.is_question:
                    queryset.append(article)
        if interest == 'live':
            queryset_, queryset = queryset, []
            for article in queryset_:
                delta = (datetime.now() - article.created_at.replace(tzinfo=None))
                if delta <= timedelta(days=1):
                    queryset.append((article,
                                     UserArticle.objects.filter(article=article, like=True).count(),
                                     Comment.objects.filter(article=article).count()))

            queryset_ = sorted(queryset, key=lambda x: x[1]+x[2], reverse=True)
            queryset.clear()
            for query in queryset_:
                queryset.append(query[0])
        elif interest:
            queryset_, queryset = queryset, []
            required_likes = {'hot': 5, 'best': 50}
            if interest in required_likes:
                for article in queryset_:
                    if UserArticle.objects.filter(article=article, like=True).count() >= required_likes[interest]:
                        queryset.append(article)
            else:
                queryset = queryset_
        return queryset


class ArticleViewSet_My_All(ArticleViewSet):
    def list(self, request, board_id):
        if board_id == "my":
            queryset = self.get_queryset_my(request).order_by('-id')
        elif board_id == "all":
            queryset = self.get_queryset_all(request).order_by('-id')
        else:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"error": "wrong_board_id", "detail": "게시판이 존재하지 않습니다."})

        # 검색 기능
        #search = self.request.query_params.get('search', None)
        #queryset = self.get_queryset_search(search, queryset)

        # Hot 게시물, Best 게시물
        #interest = self.request.query_params.get('interest', None)
        #queryset = self.get_queryset_interest(interest, queryset)

        search = self.request.query_params.get('search', None)
        interest = self.request.query_params.get('interest', None)

        # 검색 기능
        if search:
            queryset = self.get_queryset_search(search, queryset)
        # Hot 게시물, Best 게시물
        elif interest:
            queryset = self.get_queryset_interest(interest, queryset)
        elif interest and search:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "wrong query parameter"})

        return self.paginate(request, queryset)

    def get_queryset_all(self, request):
        queryset = Article.objects.none()

        boards = Board.objects.filter(university=request.user.university)
        for board in boards:
            queryset |= Article.objects.filter(board=board)
        return queryset

    def get_queryset_my(self, request):
        interest = self.request.query_params.get('interest', None)

        queryset = Article.objects.none()
        if not interest or interest == "article":
            queryset = Article.objects.filter(writer=request.user)

        elif interest == "comment":
            for comment in Comment.objects.filter(commenter=request.user):
                queryset |= Article.objects.filter(id=comment.article.id)

        elif interest == "scrap":
            for user_article in UserArticle.objects.filter(user=request.user, scrap=True):
                queryset |= Article.objects.filter(id=user_article.article.id)

        return queryset


class UserArticleView(viewsets.GenericViewSet):
    serializer_class = UserArticleSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # POST /like/article/{article_id}
    def create(self, request, article_id):
        article = Article.objects.get_or_none(id=article_id)

        if not article:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"error": "wrong_article_id", "detail": "게시글이 존재하지 않습니다."})

        if not (user_article := UserArticle.objects.get_or_none(user=request.user, article=article)):
            serializer = self.get_serializer(data={})
            serializer.is_valid(raise_exception=True)
            user_article = serializer.save()
        else:
            user_article = UserArticle.objects.get(user=request.user, article=article)
            serializer = self.get_serializer(user_article, data={}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.update(user_article, serializer.validated_data)
        return self.get_response(article, user_article)

    def get_response(self, article):
        return Response(status=status.HTTP_200_OK)



class UserArticleLikeView(UserArticleView):
    def get_response(self, article, user_article):
        return Response(status=status.HTTP_200_OK,
                        data={
                            "like": UserArticle.objects.filter(article=article, like=True).count(),
                            "detail": "이 글을 공감하였습니다."
                            }
                        )


class UserArticleScrapView(UserArticleView):
    def get_response(self, article, user_article):
        return Response(status=status.HTTP_200_OK,
                        data={
                            "scrap": UserArticle.objects.filter(article=article, scrap=True).count(),
                            "detail": "이 글을 스크랩하였습니다." if user_article.scrap else "스크랩을 취소하였습니다."
                            }
                        )

class UserArticleSubscribeView(UserArticleView):
    def get_response(self, article, user_article):
        return Response(status=status.HTTP_200_OK,
                        data={
                            "subscribe": user_article.subscribe,
                            "detail": "댓글 알림을 켰습니다." if user_article.subscribe else "댓글 알림을 껐습니다."
                            }
                        )