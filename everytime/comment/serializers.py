from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status
from comment.models import Comment
from article.models import Article

from django.utils import timezone
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
        )

    def get_is_mine(self, obj):
        return obj.commenter == self.context['request'].user

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at).strftime('%m/%d %H:%M')
    
    def get_user_nickname(self, obj):
        if obj.is_anonymous is True:
            return '익명(글쓴이)'
        else:
            return obj.commenter.nickname