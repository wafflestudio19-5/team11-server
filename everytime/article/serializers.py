from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from university.models import University
from article.models import Article

from .models import Board

class ArticleCreateSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required = True)
    text = serializers.CharField(required = True)
    is_anonymous = serializers.BooleanField(required=True)
    is_question = serializers.BooleanField(required=True)
    board = serializers.IntegerField()
    
    class Meta:
        model = Article
        fields = '__all__'

    def validate(self, data):

        return data

    def create(self, validated_data):
        validated_data['writer'] = self.context['request'].user
        board_id = validated_data['board']
        validated_data['board'] = Board.objects.get(id = board_id)
        article = Article.objects.create(**validated_data)
        return article

class ArticleSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    text = serializers.CharField()
    user_nickname = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    image_count = serializers.SerializerMethodField()
    class Meta:
        model = Article
        fields = ('id', 'title', 'text', 'user_nickname', "like_count", "comment_count", "image_count")
    
    def get_user_nickname(self, obj):
        return obj.writer.nickname
    
    def get_like_count(self, obj):
        return 0

    def get_comment_count(self, obj):
        return 0

    def get_image_count(self, obj):
        return 0
