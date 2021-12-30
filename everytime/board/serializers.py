from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Board
from university.models import University
from article.serializers import *

class BoardSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    university = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices = Board.BoardType.choices)
    description = serializers.CharField(allow_blank =True)
    allow_anonymous = serializers.BooleanField()

    class Meta:
        model = Board
        fields = ('id', 'name', 'university', 'type', 'description', 'allow_anonymous',)

    def validate(self, data):
        
        # create 시의 logic
        if self.instance == None:
            # superuser가 아니면 설정 제한
            if not self.context['request'].user.is_superuser:
                data['university'] = self.context['request'].user.university.name
                data['type'] = 5
            elif 'university' not in data:
                data['university'] = self.context['request'].user.university.name

            # 존재하지 않는 대학
            try:
                university = University.objects.get(name=data['university'])
            except ObjectDoesNotExist:
                raise serializers.ValidationError({"detail": "No such university exists"})

            # 이미 존재하는 게시판
            if len(Board.objects.filter(name=data['name'], university=university)):
                raise serializers.ValidationError({"detail": "This Board has already exists in this university"})
        else:
            return {'description' : data['description']}

        return data


    def create(self, validated_data):
        validated_data['university'] = University.objects.get(name=validated_data['university'])
        validated_data['manager'] = self.context['request'].user
        board = Board.objects.create(**validated_data)
        return board

    def update(self, instance, validated_data):

        user = self.context['request'].user
        if user != instance.manager or not user.is_superuser:
            raise PermissionDenied('권한이 없습니다.')

        super().update(instance, validated_data)

        
class BoardNameSerializer(BoardSerializer):
    university = serializers.SerializerMethodField()
    class Meta(BoardSerializer.Meta):
        pass
    
    def get_university(self, board):
        return board.university.name

class BoardGetSeriallizer(serializers.ModelSerializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=Board.BoardType.choices)
    description = serializers.CharField()

    class Meta:
        model = Board
        fields = ('id', 'name', 'type', 'description',)

# Article list로 대체
# class BoardListSeriallizer(serializers.Serializer):
#     articles = serializers.SerializerMethodField()
#     class Meta:
#         fields = ('articles')

#     def get_articles(self, board):
#         articles = ArticleSerializer(board.article.filter(), many=True).data
#         return articles
        


