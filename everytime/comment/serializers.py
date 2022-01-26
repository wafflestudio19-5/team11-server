from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status
from comment.models import Comment, UserComment
from article.models import Article, UserArticle

from django.utils import timezone
from common.custom_exception import CustomException

class CommentCreateSerializer(serializers.ModelSerializer):

    parent = serializers.IntegerField()
    text = serializers.CharField(required = True)
    is_anonymous = serializers.BooleanField()
    class Meta:
        model =  Comment
        fields = ('parent','text','is_anonymous',)

    def validate(self, data):
        return_data = data
        parent = return_data.get('parent')
        if parent in ('',0):
            return_data.pop('parent')
            parent = None
        if parent and Comment.objects.get_or_none(id=parent)==None:
            raise ValidationError(({'detail': '원댓글이 존재하지 않습니다.'}))
        
        return return_data

    def create(self, validated_data):
        if 'parent' in validated_data:
            validated_data['parent'] = Comment.objects.get(id=validated_data['parent'])

        article = Article.objects.get_or_none(id=self.context['article_id'])
        validated_data['article'] = article
        validated_data['is_writer'] = (
            self.context['request'].user == article.writer
        )
        validated_data['commenter'] = self.context['request'].user
        validated_data['is_subcomment'] = ('parent' in validated_data.keys())

        comment = Comment.objects.create(**validated_data)
        if 'parent' not in validated_data:
            comment.parent = comment
        comment.save()
        return comment

class CommentSerializer(serializers.ModelSerializer):
    is_mine = serializers.SerializerMethodField()
    created_at = serializers.SerializerMethodField()
    user_nickname = serializers.SerializerMethodField()
    user_image = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    has_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            'id',
            'parent',
            'is_subcomment',
            'is_mine',
            'text',
            'created_at',
            'like_count',
            'is_writer',
            'user_nickname', 
            'user_image',
            'has_subscribed',
        )

    def get_is_mine(self, obj):
        return obj.commenter == self.context['request'].user

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime('%m/%d %H:%M')
    
    def get_user_nickname(self, obj):
        if obj.commenter == None or obj.commenter.is_active == False:
            return '(알수없음)'
        if obj.is_active == False:
            return "(삭제)"
        if obj.is_anonymous is True:
            user_article = UserArticle.objects.get_or_none(article=obj.article, user=obj.commenter)
            if user_article==None:
                return '익명'
            elif obj.is_writer is True and user_article.nickname_code == 0:
                return '익명(글쓴이)'
            elif user_article.nickname_code != None:
                return f'익명{str(user_article.nickname_code)}'
            else:
                return '익명'
        else:
            return obj.commenter.nickname

    def get_user_image(self, obj):
        if obj.commenter != None and obj.commenter.is_active == True:
            if obj.is_anonymous == False and obj.commenter.profile_image:
                return obj.commenter.profile_image.url
            else:
                 return ""
        else:
            return ""
    
    def get_like_count(self, obj):
        return UserComment.objects.filter(comment = obj, like = True).count()

    def get_has_subscribed(self, obj):
        return bool(UserComment.objects.get_or_none(user=self.context['request'].user, subscribe=True, comment=obj))

class UserCommentSerializer(serializers.ModelSerializer):
    like = serializers.BooleanField(required=False)
    subscribe = serializers.BooleanField(required=False)

    class Meta:
        model = UserComment
        fields = ('id', 'like', 'subscribe',)

    def validate(self, data):
        action = self.context['view'].basename 
        if self.instance == None:
            if action == 'comment_like':
                return {'like' : True}
            elif action == 'comment_subscribe':
                return {'subscribe' : True}
            return {}
        else:
            if action == 'comment_like' and self.instance.like == True:
                raise CustomException("이미 공감한 댓글입니다.", status.HTTP_400_BAD_REQUEST)
            elif action == 'comment_subscribe':
                return {'subscribe' : not self.instance.subscribe}
            return {}

    def create(self, validated_data):
        comment_id = self.context['view'].kwargs['comment_id']
        validated_data['comment'] = Comment.objects.get(id = comment_id)
        validated_data['user'] = self.context['request'].user
        user_comment = UserComment.objects.create(**validated_data)
        return user_comment