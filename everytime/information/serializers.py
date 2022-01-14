from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status
from django.db import transaction
from django.utils import timezone

from article.models import Article
from comment.models import Comment
from .models import *
from lecture.models import *
from comment.serializers import CommentSerializer

from common.custom_exception import CustomException

class InformationCreateSerializer(serializers.ModelSerializer):
    subject_professor = serializers.IntegerField()
    lecture = serializers.IntegerField()
    test_number = serializers.IntegerField()  # 기타는 0번
    test_method = serializers.IntegerField()
    strategy = serializers.CharField(max_length=1000)
    problems = serializers.CharField(max_length=1000)

    class Meta:
        model = Information
        fields = ('subject_professor', 'lecture',
                  'test_number', 'test_method', 'strategy', 'problems')

    def validate(self, data):
        user = self.context['request'].user


        if not (subject_professor := SubjectProfessor.objects.get_or_none(id=data['subject_professor'])):
            raise CustomException("존재하지 않는 SubjectProfessor 입니다.", status.HTTP_404_NOT_FOUND)
        if not subject_professor.professor:
            raise CustomException("Professor가 NULL인 SubjectProfessor입니다. ", status.HTTP_400_BAD_REQUEST)
        if not (lecture := Lecture.objects.get_or_none(id=data['lecture'])):
            raise CustomException("존재하지 않는 Lecture입니다.", status.HTTP_404_NOT_FOUND)
        if subject_professor != lecture.subject_professor:
            raise CustomException("Lecture가 SubjectProfessor에 포함되지 않습니다.", status.HTTP_409_CONFLICT)

        if Information.objects.filter(user=user, lecture=lecture):
            raise CustomException("이미 강의평을 작성한 적이 있습니다.", status.HTTP_409_CONFLICT)

        return data

    def create(self, validated_data):
        validated_data.pop('subject_professor')
        validated_data['lecture'] = Lecture.objects.get(id=validated_data['lecture'])
        validated_data['user'] = self.context['request'].user

        return Information.objects.create(**validated_data)

class InformationViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subject_professor_id = serializers.SerializerMethodField()
    lecture_id = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    test_number = serializers.IntegerField()  # 기타는 0번
    test_method = serializers.SerializerMethodField()
    strategy = serializers.CharField(max_length=1000)
    problems = serializers.CharField(max_length=1000)

    class Meta:
        model = Information
        fields = ('id', 'subject_professor_id', 'lecture_id', 'year', 'season', 'test_number', 'test_method', 'strategy', 'problems')

    def get_lecture_id(self, obj):
        return obj.lecture.id

    def get_subject_professor_id(self, obj):
        return obj.lecture.subject_professor.id

    def get_year(self, obj):
        return obj.lecture.year

    def get_season(self, obj):
        return Lecture.SeasonCode[obj.lecture.season]

    def get_test_method(self, obj):
        return Information.TestMethodCode[obj.test_method]

