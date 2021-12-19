from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Post
from .serializers import PostCreateSerializer, PostSerializer, PostUpdateSerializer
from .models import PostImage, UserPost
from university.models import University
from .models import Board

# Create your views here.

def UniversityPosts(university):
    searhcedPosts = []
    for board in university.university_boards.filter():
        posts = board.board_posts.filter(is_active=True)
        searhcedPosts += posts
    searhcedPosts.reverse()
    return searhcedPosts


class WritePost(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        post = serializer.save()
        return Response(PostSerializer(post, context={'request': request}).data, status=status.HTTP_201_CREATED)

    def put(self, request):
        id = request.data['id']

        post = Post.objects.get(id=id)
        postData = PostUpdateSerializer(post).data

        for i in ('title', 'content', 'is_anonymous'):
            if i in request.data:
                postData[i] = request.data[i]

        serializer = PostUpdateSerializer(data=postData, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(post, serializer.validated_data)

        return Response(PostSerializer(post, context={'request': request}).data, status=status.HTTP_200_OK)

    def delete(self, request):
        id = request.data['id']
        post = Post.objects.get(id=id)
        post.is_active = False
        post.save()
        return Response(status=status.HTTP_200_OK)

class DeletePostImage(APIView):
    permission_classes = (permissions.AllowAny,)
    def delete(self, request):
        id = request.data['id']
        postImage = PostImage.objects.get(id=id)
        postImage.is_active = False
        postImage.save()
        return Response(status=status.HTTP_200_OK)

class GetPost(APIView):
    permissions_classes = (permissions.AllowAny,)
    def get(self, request):
        id = request.data['id']
        post = Post.objects.get(id=id)

        return Response(PostSerializer(post, context={'request': request}).data, status=status.HTTP_200_OK)

class SearchPostTitle(APIView):
    # 유저가 속한 대학에서 제목이 일치하는 post를 검색
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        #찾고자 하는 글의 제목
        if "title" not in request.data:
            return Response({"title": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        title = request.data['title']
        #검색된 글들을 저장
        searhcedPosts = []
        #유저가 속한 대학
        university = self.request.user.university
        #대학에 속한 모든 Post에 대해
        for post in UniversityPosts(university):
            if post.title == title:
                searhcedPosts.append(post)

        return Response(PostSerializer(searhcedPosts, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class SearchPostKeyword(APIView):
    # 유저가 속한 대학에서 제목이 일치하는 post를 검색
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request):
        #찾고자 하는 글의 제목
        if "keyword" not in request.data:
            return Response({"keyword": "This field is required"}, status=status.HTTP_400_BAD_REQUEST)
        keyword = request.data['keyword']
        #검색된 글들을 저장
        searhcedPosts = []
        #유저가 속한 대학
        university = self.request.user.university
        #대학에 속한 모든 Post에 대해
        for post in UniversityPosts(university):
            if keyword in (post.title+"\n"+post.content):
                searhcedPosts.append(post)
        return Response(PostSerializer(searhcedPosts, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /post/'}, status=status.HTTP_200_OK)
