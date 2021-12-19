from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostCreateSerializer, PostSerializer
from .models import PostImage, UserPost
from university.models import University
from .models import Board

# Create your views here.
class WritePost(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):

        serializer = PostCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        post = serializer.save()

        return Response(status=status.HTTP_201_CREATED)

class SearchPost(APIView):
    permission_classes = (permissions.AllowAny,)
    def get(self, request):

        title = request.data['title']
        print(title+"?")
        return Response(PostSerializer(Post.objects.filter(title=title), many=True, context={'request': request}).data, status=status.HTTP_200_OK)

class PostViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /post/'}, status=status.HTTP_200_OK)
