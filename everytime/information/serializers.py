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
    year = serializers.IntegerField()
    season = serializers.IntegerField()
    test_number = serializers.IntegerField()  # 기타는 0번
    test_method = serializers.CharField(max_length=150)
    strategy = serializers.CharField(max_length=1000)
    problems = serializers.CharField(max_length=1000)

    class Meta:
        model = Information
        fields = ('subject_professor', 'year', 'season',
                  'test_number', 'test_method', 'strategy', 'problems')

    def validate(self, data):
        user = self.context['request'].user
        year, season, test_number= data['year'], data['season'], data['test_number']

        if not (subject_professor := SubjectProfessor.objects.get_or_none(id=data['subject_professor'])):
            raise CustomException("존재하지 않는 SubjectProfessor 입니다.", status.HTTP_404_NOT_FOUND)
        if not subject_professor.professor:
            raise CustomException("Professor가 NULL인 SubjectProfessor입니다. ", status.HTTP_400_BAD_REQUEST)
        if not Lecture.objects.filter(subject_professor=subject_professor, year=year, season=season):
            raise CustomException("해당 학기에 강의가 없습니다. ", status.HTTP_404_NOT_FOUND)
        if Information.objects.filter(user=user, year=year, season=season, test_number=test_number, subject_professor=subject_professor):
            raise CustomException("이미 시험정보를 작성한 적이 있습니다.", status.HTTP_409_CONFLICT)

        return data

    def create(self, validated_data):
        validated_data['subject_professor'] = SubjectProfessor.objects.get(id=validated_data['subject_professor'])
        validated_data['user'] = self.context['request'].user

        return Information.objects.create(**validated_data)

class InformationViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subject_professor_id = serializers.SerializerMethodField()
    year = serializers.IntegerField()
    season = serializers.SerializerMethodField()
    test_number = serializers.IntegerField()  # 기타는 0번
    test_method = serializers.SerializerMethodField()
    strategy = serializers.CharField(max_length=1000)
    problems = serializers.CharField(max_length=1000)

    class Meta:
        model = Information
        fields = ('id', 'subject_professor_id', 'year', 'season', 'test_number', 'test_method', 'strategy', 'problems')


    def get_subject_professor_id(self, obj):
        return obj.subject_professor.id

    def get_season(self, obj):
        return Lecture.SeasonCode[obj.season]

    def get_test_method(self, obj):
        data = ""
        for i in obj.test_method.split(' '):
            data += (Information.TestMethodCode[int(i)]) + ", "
        data = data[:-2]
        return data

