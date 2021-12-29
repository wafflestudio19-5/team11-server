from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from article.models import Article

class CommentViewSet(viewsets.GenericViewSet):
    serializer_class = CommentSerializer

    #POST /board/{board_id}/article/{article_id}/comment/
    def create(self, request, board_id, article_id):
        
        if not (article := Article.objects.get_or_none(id=article_id)):
            return Response(status=status.HTTP_404_NOT_FOUND, 
                            data={ "error":"wrong_article_id", "detail" : "게시글이 존재하지 않습니다."})

        data = request.data.copy()
        data['board'] = board_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        article = serializer.save()

        # MODEL FIELD
        # article = models.ForeignKey(Article, on_delete=models.CASCADE) 
        # parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
        # text = models.CharField(max_length=300, null = False)
        # created_at = models.DateTimeField(auto_now_add=True)
        # commenter = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null = True)
        # like_count = models.PositiveIntegerField(default=0)
        # is_writer = models.BooleanField(default=False, null = False)
        # is_anonymous = models.BooleanField(default=True, null = False)
        # is_active = models.BooleanField(default=True, null = False)

        # REQUEST 
        # "parent_id" : Int(Nullable) // 대댓글 작성시 원댓글 id
		# "text" : String, // "댓글 내용",
		# "is_anonymous" : Boolean // True or False



        return Response(status=status.HTTP_200_OK, data="POST comment")

    #DELETE /board/{board_id}/article/{article_id}/comment/{comment_id}
    def destroy(self, request, board_id, article_id, pk):
        return Response(status=status.HTTP_200_OK, data="DELETE comment")
