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
    test_type = serializers.IntegerField()  # 기타는 0번
    test_method = serializers.CharField(max_length=100)
    strategy = serializers.CharField(max_length=1000)
    problems = serializers.ListField(required=False)

    class Meta:
        model = Information
        fields = ('subject_professor', 'year', 'season', 'test_method', 'test_type', 'strategy', 'problems')
        extra_fields = ['problems']

    def validate(self, data):
        user = self.context['request'].user
        year, season, test_method= data['year'], data['season'], data['test_method']

        if not (subject_professor := SubjectProfessor.objects.get_or_none(id=data['subject_professor'])):
            raise CustomException("존재하지 않는 SubjectProfessor 입니다.", status.HTTP_404_NOT_FOUND)
        if not subject_professor.professor:
            raise CustomException("Professor가 NULL인 SubjectProfessor입니다. ", status.HTTP_400_BAD_REQUEST)
        if not Lecture.objects.filter(subject_professor=subject_professor, year=year, season=season):
            raise CustomException("해당 학기에 강의가 없습니다. ", status.HTTP_404_NOT_FOUND)
        if Information.objects.filter(user=user, year=year, season=season, subject_professor=subject_professor, test_method=test_method):
            raise CustomException("이미 시험정보를 작성한 적이 있습니다.", status.HTTP_409_CONFLICT)

        return data

    def create(self, validated_data):
        validated_data['subject_professor'] = SubjectProfessor.objects.get(id=validated_data['subject_professor'])
        validated_data['user'] = self.context['request'].user

        problems = ""

        if 'problems' in validated_data:
            problem_list = validated_data.pop('problems')
            if len(problem_list) > 0:
                problems += problem_list[0]

            for i in range(1, len(problem_list)):
                problems += "\t" + problem_list[i]

        validated_data['problems'] = problems

        return Information.objects.create(**validated_data)

class InformationViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subject_professor_id = serializers.SerializerMethodField()
    year = serializers.IntegerField()
    season = serializers.SerializerMethodField()
    test_method = serializers.SerializerMethodField()  # 기타는 0번
    test_type = serializers.SerializerMethodField()
    strategy = serializers.CharField(max_length=1000)
    problems = serializers.SerializerMethodField()

    class Meta:
        model = Information
        fields = ('id', 'subject_professor_id', 'year', 'season', 'test_type', 'test_method', 'strategy', 'problems')


    def get_subject_professor_id(self, obj):
        return obj.subject_professor.id

    def get_season(self, obj):
        return Lecture.SeasonCode[obj.season]

    def get_test_method(self, obj):
        data = ""
        for i in obj.test_method.split(' '):
            data += i + ", "
        data = data[:-2]
        return data

    def get_test_type(self, obj):
        return Information.TestType[obj.test_type]

    def get_problems(self, obj):
        return obj.problems.split('\t')