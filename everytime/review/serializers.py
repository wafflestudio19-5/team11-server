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

class ReviewCreateSerializer(serializers.ModelSerializer):
    subject_professor = serializers.IntegerField()
    year = serializers.IntegerField()
    season = serializers.IntegerField()
    rating = serializers.IntegerField()
    homework = serializers.IntegerField()
    team_activity = serializers.IntegerField()
    grading = serializers.IntegerField()
    attendance = serializers.IntegerField()
    test_count = serializers.IntegerField()
    comment = serializers.CharField(max_length=1000)

    class Meta:
        model = Review
        fields = ('subject_professor', 'year', 'season', 'rating', 'homework',
                  'team_activity', 'grading', 'attendance', 'test_count', 'comment')

    def validate(self, data):
        user = self.context['request'].user
        year, season = data['year'], data['season']

        if not (subject_professor := SubjectProfessor.objects.get_or_none(id=data['subject_professor'])):
            raise CustomException("존재하지 않는 SubjectProfessor 입니다.", status.HTTP_404_NOT_FOUND)
        if not subject_professor.professor:
            raise CustomException("Professor가 NULL인 SubjectProfessor입니다. ", status.HTTP_400_BAD_REQUEST)
        if not Lecture.objects.filter(subject_professor=subject_professor, year=year, season=season):
            raise CustomException("해당 학기에 강의가 없습니다. ", status.HTTP_404_NOT_FOUND)
        if Review.objects.filter(user=user, year=year, season=season, subject_professor=subject_professor):
            raise CustomException("이미 강의평을 작성한 적이 있습니다.", status.HTTP_409_CONFLICT)

        return data

    def create(self, validated_data):
        validated_data['subject_professor'] = SubjectProfessor.objects.get(id=validated_data['subject_professor'])
        validated_data['user'] = self.context['request'].user

        return Review.objects.create(**validated_data)

class ReviewViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subject_professor_id = serializers.SerializerMethodField()
    year = serializers.IntegerField()
    season = serializers.SerializerMethodField()
    homework = serializers.SerializerMethodField()
    team_activity = serializers.SerializerMethodField()
    grading = serializers.SerializerMethodField()
    attendance = serializers.SerializerMethodField()
    test_count = serializers.SerializerMethodField()
    rating = serializers.IntegerField()
    comment = serializers.CharField()

    class Meta:
        model = Review
        fields = '__all__'


    def get_subject_professor_id(self, obj):
        return obj.subject_professor.id

    def get_season(self, obj):
        return Lecture.SeasonCode[obj.season]

    def get_homework(self, obj):
        return Review.HomeworkCode[obj.homework]
    
    def get_team_activity(self, obj):
        return Review.TeamActivityCode[obj.team_activity]

    def get_grading(self, obj):
        return Review.GradingCode[obj.grading]
    
    def get_attendance(self, obj):
        return Review.AttendanceCode[obj.attendance]

    def get_test_count(self, obj):
        return Review.TestCountCode[obj.test_count]