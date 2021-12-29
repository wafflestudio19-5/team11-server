from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action
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

        return Response(status=status.HTTP_200_OK, data=ArticleSerializer(article).data)

    #DELETE /board/{board_id}/article/{pk}/
    def destroy(self, request, board_id, pk=None):
        if not (board := Board.objects.get_or_none(id=board_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_board_id", "detail" : "게시판이 존재하지 않습니다."})
        if not (article := Article.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_article_id", "detail" : "게시글이 존재하지 않습니다."})
        
        print("break 1")
        board = Board.objects.get(id=board_id)
        article = Article.objects.get(id = pk)
        print("break 2")

        if article.board != board:
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_match", "detail" : "해당 게시판의 게시글이 아닙니다."})
        article.delete()
        
        print("break 3")

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
