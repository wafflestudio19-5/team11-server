from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status
from django.db import transaction
from django.utils import timezone

from article.models import Article
from comment.models import Comment
from .models import *
from comment.serializers import CommentSerializer

from common.custom_exception import CustomException

class CustomLectureCreateSerializer(serializers.ModelSerializer):

    lecture = serializers.IntegerField()
    memo = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = CustomLecture
        fields = ('lecture', 'memo')

    def validate(self, data):
        #user = self.context['request'].user

        schedule = self.context['schedule']

        if not schedule:
            raise CustomException("존재하지 않는 시간표입니다. ", status.HTTP_404_NOT_FOUND)

        lecture = Lecture.objects.get_or_none(id=data['lecture'], year=schedule.year, season=schedule.season)
        if not lecture:
            raise CustomException("존재하지 않는 강의입니다. ", status.HTTP_404_NOT_FOUND)

        return data

    def create(self, validated_data):
        #validated_data['user'] = self.context['request'].user
        validated_data['schedule'] = self.context['schedule']

        lecture = Lecture.objects.get(id=validated_data['lecture'])
        validated_data['lecture'] = lecture

        validated_data['nickname'] = lecture.subject_professor.subject_name
        validated_data['professor'] = lecture.subject_professor.professor
        validated_data['time'] = lecture.time
        validated_data['location'] = lecture.location

        return CustomLecture.objects.create(**validated_data)

class CustomLectureCreateSerializer_Custom(serializers.ModelSerializer):

    nickname = serializers.CharField(max_length=100)
    professor = serializers.CharField(max_length=100)
    time = serializers.CharField(max_length=100)
    location = serializers.CharField(max_length=100)
    memo = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = CustomLecture
        fields = ('nickname', 'professor', 'time', 'location', 'memo')

    def validate(self, data):

        print(data)

        schedule = self.context['schedule']

        if not schedule:
            raise CustomException("존재하지 않는 시간표입니다. ", status.HTTP_404_NOT_FOUND)

        return data

    def create(self, validated_data):
        #validated_data['user'] = self.context['request'].user
        validated_data['schedule'] = self.context['schedule']

        return CustomLecture.objects.create(**validated_data)

class CustomLecturePutSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=100, required=False)
    memo = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = CustomLecture
        fields = ('nickname', 'memo')

    def update(self, instance, validated_data):
        #
        result = super().update(instance, validated_data)
        instance.save()
        print(instance.nickname)
        return result

class CustomLectureViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    lecture = serializers.SerializerMethodField()
    nickname = serializers.CharField()
    professor = serializers.CharField()
    time = serializers.CharField()
    location = serializers.CharField()
    memo = serializers.CharField()

    class Meta:
        model = Schedule
        fields = ('id', 'lecture', 'nickname', 'professor', 'time', 'location', 'memo')

    def get_lecture(self, obj):
        if not obj.lecture:
            return None
        return obj.lecture.id
