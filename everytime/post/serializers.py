from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from .models import Post, PostImage, UserPost
from board.models import Board
from university.models import University
from user.serializers import UserNicknameSerializer

class PostImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = PostImage
        fields = ['image']



class PostSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    writer = serializers.SerializerMethodField()
    class Meta:
        model = Post
        fields = ['id', 'board', 'title', 'content', 'created_at', 'is_anonymous', 'images', 'writer']

    def get_writer(self, instance):
        userPost = UserPost.objects.filter(post=instance, is_owner=True)
        if userPost:
            user = UserPost.objects.get(post=instance, is_owner=True).user
            nickname = user.nickname
            id = user.id
            return {"id": id, "nickname": nickname, }
        return "Anonymous"

    def get_images(self, instance):
        return PostImageSerializer(instance.post_postImages.filter(), many=True, context=self.context).data
    #def get_user(self, instance):




class PostCreateSerializer(serializers.ModelSerializer):
    board = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('id', 'board', 'title', 'content', 'created_at', 'is_anonymous')

    def validate(self, data):
        # board, title, content 정보를 포함해야 함
        error = {}
        for i in ('board', 'title', 'content', 'is_anonymous'):
            if i not in data:
                error[i] = "field is required"
        if error:
            raise serializers.ValidationError(error)
        # 존재하지 않는 게시판
        try:
            board = University.objects.get(id=data['board'])
        except ObjectDoesNotExist:
            raise serializers.ValidationError({"status": "No such university exists"})
        return data

    def create(self, validated_data):
        board = Board.objects.get(id=validated_data['board'])
        post = Post.objects.create(board=board, title=validated_data['title'], content=validated_data['content'], is_anonymous=validated_data['is_anonymous'])

        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            PostImage.objects.create(post=post, image=image_data)

        user = self.context['request'].user
        UserPost.objects.create(user=user, post=post, is_owner=True)

        return post



