from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from university.models import University
from board.models import Board
#from .models import Article

# Create your views here.
class ArticleViewSet(viewsets.GenericViewSet):
    serializer_class = ArticleCreateSerializer
    permission_classes = (permissions.AllowAny,)
   
    #POST /board/{board_id}/article/
    def create(self, request, board_id):

        if not (board := Board.objects.get_or_none(id=board_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_board_id", "detail" : "게시판이 존재하지 않습니다."})

        data = request.data.copy()
        data['board'] = board_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()

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
        article.delete()

        return Response(status=status.HTTP_200_OK, data={"success" : True})

    #GET /board/{board_id}/article/?offset=[offset]&?limit=[limit]
    def list(self, request, board_id):
        if not (board := Board.objects.get_or_none(id=board_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_board_id", "detail" : "게시판이 존재하지 않습니다."})
        
        queryset =  self.get_queryset().filter(board_id=board_id).order_by('-id')
        page = self.paginate_queryset(queryset) 

        if page is not None: 
            serializer = ArticleSerializer(page, many=True) 
            return self.get_paginated_response(serializer.data) 
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")

    def get_queryset(self): 
        queryset = Article.objects.all() 
        return queryset

class UserArticleView(viewsets.GenericViewSet):
    serializer_class = UserArticleSerializer
    permission_classes = (permissions.AllowAny,)

    #POST /like/article/{article_id}
    def create(self, request, article_id):
        article = Article.objects.get_or_none(id=article_id)

        if not article:
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_article_id", "detail" : "게시글이 존재하지 않습니다."})

        if not (user_article := UserArticle.objects.get_or_none(user = request.user, article = article)):
            serializer = self.get_serializer(data={})
            serializer.is_valid(raise_exception=True)
            user_article = serializer.save()
        else:
            user_article = UserArticle.objects.get(user = request.user, article = article)
            serializer = self.get_serializer(user_article, data={}, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.update(user_article, serializer.validated_data)
        return self.get_response(article, user_article.scrap)
        
    def get_response(self, article):
        return Response(status=status.HTTP_200_OK)

class UserArticleLikeView(UserArticleView):
    def get_response(self, article, scrap):
        return Response(status=status.HTTP_200_OK, 
                        data={
                            "like" : UserArticle.objects.filter(article = article, like = True).count(),
                            "detail" : "이 글을 공감하였습니다."  
                            }
                        )

class UserArticleScrapView(UserArticleView):
    def get_response(self, article, scrap):
        return Response(status=status.HTTP_200_OK, 
                        data={
                            "scrap" : UserArticle.objects.filter(article = article, scrap = True).count(),
                            "detail" : "이 글을 스크랩하였습니다." if scrap else "스크랩을 취소하였습니다."  
                            }
                        )
