from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status
from django.db import transaction
from django.utils import timezone

from article.models import Article
from comment.models import Comment
from .models import *
from comment.serializers import CommentSerializer

from common.custom_exception import CustomException

class ScheduleCreateSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=100)
    year = serializers.IntegerField()
    season = serializers.IntegerField()

    class Meta:
        model = Schedule
        fields = ('name', 'year', 'season')

    def validate(self, data):
        user = self.context['request'].user

        schedule = Schedule.objects.get_or_none(name=data['name'], user=user, year=data['year'], season=data['season'])
        if schedule:
            raise CustomException("이미 존재하는 시간표명입니다. ", status.HTTP_409_CONFLICT)

        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user

        return Schedule.objects.create(**validated_data)

class ScheduleViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    year = serializers.IntegerField()
    season = serializers.IntegerField()
    last_visit = serializers.DateTimeField()

    class Meta:
        model = Schedule
        fields = ('id', 'name', 'year', 'season', 'last_visit')


class ScheduleNameSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Schedule
        fields = ('name', )
