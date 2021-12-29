from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status
from comment.models import Comment
from article.models import Article

class CommentCreateSerializer(serializers.ModelSerializer):

    parent = serializers.CharField(allow_blank=True)
    text = serializers.CharField(required = True)
    is_anonymous = serializers.BooleanField()
    class Meta:
        model =  Comment
        fields = ('parent','text','is_anonymous')

    def validate(self, data):
        parent=data.get('parent')
        if parent in ("", 0):
            parent = None
            data.pop('parent')

        if 'parent' in data and Comment.objects.get_or_none(id=parent)==None:
            raise ValidationError(({"detail": "원댓글이 존재하지 않습니다."}))
        
        return data

    def create(self, validated_data):
        if 'parent' in validated_data:
            validated_data['parent'] = Comment.objects.get(id=validated_data['parent'])

        article = Article.objects.get_or_none(id=self.context['article_id'])
        validated_data['article'] = article
        validated_data['is_writer'] = (
            self.context['request'].user == article.writer
        )
        validated_data['commenter'] = self.context['request'].user

        comment = Comment.objects.create(**validated_data)
        return comment

class CommentSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    text = serializers.CharField()
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'title', 'text', 'user_nickname')
    
    def get_user_nickname(self, obj):
        return obj.writer.nickname