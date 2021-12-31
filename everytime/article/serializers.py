from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status
from article.models import Article
from comment.models import Comment
from .models import Board, UserArticle
from comment.serializers import CommentSerializer

from django.utils import timezone
from common.custom_exception import CustomException

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
    created_at = serializers.SerializerMethodField()
    f_created_at = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = (
            'id', 
            'title', 
            'text', 
            'user_nickname', 
            'like_count', 
            'comment_count', 
            'image_count',
            'created_at', 
            'f_created_at',
        )
    
    def get_user_nickname(self, obj):
        return obj.writer.nickname
    
    def get_like_count(self, obj):
        return UserArticle.objects.filter(article = obj, like = True).count()

    def get_comment_count(self, obj):
        return Comment.objects.filter(article = obj).count()

    def get_image_count(self, obj):
        return 0

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime("%m/%d %H:%M")

    # strftime format - https://ponyozzang.tistory.com/626
    # timezone에 맞게 출력 - https://devlog.jwgo.kr/2020/10/28/using-timezone-in-django/
    def get_f_created_at(self, obj):
        local_created_at = timezone.localtime(obj.created_at)
        return time_formatting(local_created_at)

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
            if action == 'article_like':
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