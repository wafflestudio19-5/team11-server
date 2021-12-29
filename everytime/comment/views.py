from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from board.models import Board

from .serializers import *
from article.models import Article

class CommentViewSet(viewsets.GenericViewSet):
    serializer_class = CommentCreateSerializer

    #POST /board/{board_id}/article/{article_id}/comment/
    def create(self, request, board_id, article_id):
        if not (board := Board.objects.get_or_none(id=board_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_board_id", "detail" : "게시판이 존재하지 않습니다."})
        if not (article := Article.objects.get_or_none(id=article_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_article_id", "detail" : "게시글이 존재하지 않습니다."})
        
        board = Board.objects.get(id=board_id)
        article = Article.objects.get(id = article_id)

        if article.board != board:
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_match", "detail" : "해당 게시판의 게시글이 아닙니다."})

        data = request.data.copy()
        serializer = CommentCreateSerializer(data=data, context={'request': request, 'article_id': article_id})
        serializer.is_valid(raise_exception=True)
        comment = serializer.save()

        return Response(status=status.HTTP_200_OK, data={"success" : True, "comment_id" : comment.id})

    #DELETE /board/{board_id}/article/{article_id}/comment/{comment_id}
    def destroy(self, request, board_id, article_id, pk):
        if not (board := Board.objects.get_or_none(id=board_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_board_id", "detail" : "게시판이 존재하지 않습니다."})
        if not (article := Article.objects.get_or_none(id=article_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_article_id", "detail" : "게시글이 존재하지 않습니다."})
        if not (comment := Comment.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_comment_id", "detail" : "댓글이 존재하지 않습니다."})
        
        board = Board.objects.get(id=board_id)
        article = Article.objects.get(id = article_id)
        comment = Comment.objects.get(id = pk)

        if article.board != board:
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_match", "detail" : "해당 게시판의 게시글이 아닙니다."})
        if comment.article != article:
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_match", "detail" : "해당 게시글의 댓글이 아닙니다."})

        comment.delete()

        return Response(status=status.HTTP_200_OK, data={"success" : True})
