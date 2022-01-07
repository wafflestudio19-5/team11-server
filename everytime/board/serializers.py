from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Board
from university.models import University
from article.serializers import *
from common.custom_exception import CustomException

from .models import UserBoard

class BoardSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    university = serializers.CharField(required=False)
    type = serializers.ChoiceField(choices=Board.BoardType.choices)
    description = serializers.CharField(allow_blank=True)
    allow_anonymous = serializers.BooleanField()
    is_mine = serializers.SerializerMethodField(read_only=True)
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ('id', 'name', 'university', 'type', 'description', 'allow_anonymous', 'is_mine', 'favorite')

    def get_is_mine(self, obj):
        return obj.manager == self.context['request'].user

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
                raise CustomException("대학교가 존재하지 않습니다.", status.HTTP_404_NOT_FOUND)

            # 이미 존재하는 게시판
            if len(Board.objects.filter(name=data['name'], university=university)):
                raise CustomException("중복된 이름의 게시판이 있습니다.", status.HTTP_409_CONFLICT)
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
    
    def get_favorite(self, obj):
        if self.context['request'].user.is_anonymous:
            return False
        userboard = UserBoard.objects.get_or_none(user=self.context['request'].user, board=obj)
        if not userboard:
            return obj.type == 0
        return userboard.favorite
        
class BoardGetSeriallizer(BoardSerializer):
    name = serializers.CharField()
    type = serializers.ChoiceField(choices=Board.BoardType.choices)
    description = serializers.CharField()

    class Meta:
        model = Board
        fields = ('id', 'name', 'type', 'description', 'favorite', 'university')

# Article list로 대체
# class BoardListSeriallizer(serializers.Serializer):
#     articles = serializers.SerializerMethodField()
#     class Meta:
#         fields = ('articles')

#     def get_articles(self, board):
#         articles = ArticleSerializer(board.article.filter(), many=True).data
#         return articles
        


