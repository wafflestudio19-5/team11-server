from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status
from django.db import transaction
from django.utils import timezone

from article.models import Article
from comment.models import Comment
from .models import Board, ImageArticle, UserArticle
from comment.serializers import CommentSerializer

from common.custom_exception import CustomException


import logging
logger = logging.getLogger('django')

# 시간 비교 - https://jsikim1.tistory.com/144
def time_formatting(timezone_obj):
    diff = timezone.localtime() - timezone_obj
    if diff.seconds/3600 < 1:
        diff_minutes = int(diff.seconds/60)
        return f"{diff_minutes}분 전"
    elif diff.days < 1:
        return timezone_obj.strftime("%H:%M")
    elif diff.days < 365:
        return timezone_obj.strftime("%m/%d")
    else:
        diff_years = int(diff.days/365)
        return f"{diff_years}년 전"

class ImageArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageArticle
        fields = ('image','text')

class ArticleCreateSerializer(serializers.ModelSerializer):
    texts = serializers.ListField(required = False) # list 받아오기 가능...
    title = serializers.CharField(required = True)
    text = serializers.CharField(required = True)
    is_anonymous = serializers.BooleanField(required=True)
    is_question = serializers.BooleanField(required=True)
    board = serializers.IntegerField()
    
    class Meta:
        model = Article
        fields = '__all__'
        extra_fields = ['texts']

    def validate(self, data):
        return data

    def create(self, validated_data):

        image_list = self.context.get('view').request.FILES
        validated_data['writer'] = self.context['request'].user
        board_id = validated_data['board']
        
        validated_data['board'] = Board.objects.get(id = board_id)

        with transaction.atomic():
            if 'texts' in validated_data:
                texts = validated_data.pop('texts')
            article = Article.objects.create(**validated_data)
            i = 0
            # https://donis-note.medium.com/django-rest-framework-%EB%8B%A4%EC%A4%91-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%97%85%EB%A1%9C%EB%93%9C-%EB%B0%A9%EB%B2%95-38c99d26258
            # https://www.postman.com/postman/workspace/postman-answers/request/9215231-82d960a6-ece0-42ee-88d4-eef19805860d
            for image_data in image_list.getlist('image'):
                ImageArticle.objects.create(article = article, image = image_data, description = texts[i])
                i += 1
            return article

class ArticleSerializer(serializers.ModelSerializer):
    board_id = serializers.IntegerField() #전체 게시글 열람 기능을 위함
    board_name = serializers.SerializerMethodField()
    title = serializers.CharField()
    text = serializers.CharField()
    user_nickname = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    is_mine = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    scrap_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    image_count = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    f_created_at = serializers.SerializerMethodField()
    has_scraped = serializers.SerializerMethodField()
    has_liked = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id',
            'board_id',
            'board_name',
            'title', 
            'text', 
            'user_nickname', 
            'user_image',
            'is_mine',
            'like_count', 
            'scrap_count',
            'comment_count', 
            'image_count',
            'created_at', 
            'f_created_at',
            'has_scraped',
            'has_liked',
            'images',
        )

    def get_board_name(self, obj):
        return obj.board.name

    def get_user_nickname(self, obj):
        if obj.writer == None or obj.writer.is_active == False:
            return '(알수없음)'
        if obj.is_anonymous == True:
            return '익명'
        else:
            return obj.writer.nickname
    
    def get_user_image(self, obj):
        if self.get_user_nickname(obj) == obj.writer.nickname:
            return obj.writer.profile_image

    def get_is_mine(self, obj):
        return obj.writer == self.context['request'].user
    
    def get_like_count(self, obj):
        return UserArticle.objects.filter(article = obj, like = True).count()

    def get_scrap_count(self, obj):
        return UserArticle.objects.filter(article = obj, scrap = True).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(article = obj).count()

    def get_image_count(self, obj):
        return ImageArticle.objects.filter(article = obj).count()

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime("%m/%d %H:%M")

    # strftime format - https://ponyozzang.tistory.com/626
    # timezone에 맞게 출력 - https://devlog.jwgo.kr/2020/10/28/using-timezone-in-django/
    def get_f_created_at(self, obj):
        local_created_at = timezone.localtime(obj.created_at)
        return time_formatting(local_created_at)
    
    def get_has_scraped(self, obj):
        return bool(UserArticle.objects.get_or_none(user=self.context['request'].user, scrap=True, article=obj))
    
    def get_has_liked(self, obj):
        return bool(UserArticle.objects.get_or_none(user=self.context['request'].user, like=True, article=obj))

    def get_images(self, obj):
        images = ImageArticle.objects.filter(article = obj)
        return ImageArticleSerializer(images, many = True).data

class ArticleWithCommentSerializer(ArticleSerializer):
    comments = serializers.SerializerMethodField()

    class Meta(ArticleSerializer.Meta):
        fields = ArticleSerializer.Meta.fields \
                + ('comments',)

    def get_comments(self, article):
        comments = Comment.objects.filter(article=article).order_by('parent')
        return CommentSerializer(comments, context=self.context, many=True).data

class UserArticleSerializer(serializers.ModelSerializer):
    like = serializers.BooleanField(required=False)
    scrap = serializers.BooleanField(required=False)

    class Meta:
        model = UserArticle
        fields = ('id', 'like', 'scrap',)

    def validate(self, data):
        action = self.context['view'].basename 
        if self.instance == None:
            if action == 'article_like':
                return {'like' : True}
            elif action == 'article_scrap':
                return {'scrap' : True}
            return {}
        else:
            if action == 'article_like' and self.instance.like == True:
                raise CustomException("이미 공감한 글입니다.", status.HTTP_400_BAD_REQUEST)
            elif action == 'article_scrap':
                return {'scrap' : not self.instance.scrap} # scrap과 unscrap 구현
            return {}

    def create(self, validated_data):
        article_id = self.context['view'].kwargs['article_id']
        validated_data['article'] = Article.objects.get(id = article_id)
        validated_data['user'] = self.context['request'].user
        user_article = UserArticle.objects.create(**validated_data)
        return user_article

class ImageArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageArticle
        fields = ('image', 'description')