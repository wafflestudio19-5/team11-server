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
    lecture = serializers.IntegerField()
    rating = serializers.IntegerField()
    homework = serializers.IntegerField()
    team_activity = serializers.IntegerField()
    grading = serializers.IntegerField()
    attendance = serializers.IntegerField()
    test_count = serializers.IntegerField()
    comment = serializers.CharField(max_length=1000)

    class Meta:
        model = Review
        fields = ('subject_professor', 'lecture', 'rating', 'homework',
                  'team_activity', 'grading', 'attendance', 'test_count', 'comment')

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

        if Review.objects.filter(user=user, lecture=lecture):
            raise CustomException("이미 강의평을 작성한 적이 있습니다.", status.HTTP_409_CONFLICT)

        return data

    def create(self, validated_data):
        validated_data.pop('subject_professor')
        validated_data['lecture'] = Lecture.objects.get(id=validated_data['lecture'])
        validated_data['user'] = self.context['request'].user

        return Review.objects.create(**validated_data)

class ReviewViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subject_professor_id = serializers.SerializerMethodField()
    lecture_id = serializers.SerializerMethodField()
    year = serializers.SerializerMethodField()
    season = serializers.SerializerMethodField()
    rating = serializers.IntegerField()
    comment = serializers.CharField()

    class Meta:
        model = Review
        fields = ('id', 'subject_professor_id', 'lecture_id', 'year', 'season', 'rating', 'comment')

    def get_lecture_id(self, obj):
        return obj.lecture.id

    def get_subject_professor_id(self, obj):
        return obj.lecture.subject_professor.id

    def get_year(self, obj):
        return obj.lecture.year

    def get_season(self, obj):
        return Lecture.SeasonCode[obj.lecture.season]

