from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from comment.models import Comment

class CommentCreateSerializer(serializers.ModelSerializer):

    title = serializers.CharField(required = True)
    text = serializers.CharField(required = True)
    is_anonymous = serializers.BooleanField(required=True)
    is_question = serializers.BooleanField(required=True)
    board = serializers.IntegerField()
    
    class Meta:
        model =  Comment
        fields = '__all__'

    def validate(self, data):
        
        return data

    def create(self, validated_data):
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