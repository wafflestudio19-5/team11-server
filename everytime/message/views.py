from django.shortcuts import render

from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import MessageSerializer

# Create your views here.
class MessageViewSet(viewsets.GenericViewSet):
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated,)


    #POST /message/
    def create(self, request):
        # article / comment로 시작
        # article_id or comment_id 받아옴
        # article.writer or comment.commenter와 message 시작
        return Response(status=status.HTTP_200_OK, data={"API" : "POST /message/"})

    #GET /message/{pk}/
    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_200_OK, data={"API" : "GET /message/pk/"})
    
    #GET /message/
    def list(self, request):
        return Response(status=status.HTTP_200_OK, data={"API" : "GET /message/"})

    #DELETE /message/{pk}
    def delete(self, request, pk=None):
        return Response(status=status.HTTP_200_OK, data={"API" : "DELETE /message/pk"})
