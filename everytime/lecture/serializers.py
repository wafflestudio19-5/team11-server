from re import S
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers, status
from rest_framework.exceptions import PermissionDenied, ValidationError

from .models import Lecture, SubjectProfessor
from university.models import University
from department.models import *
from article.serializers import *
from common.custom_exception import CustomException
from review.models import *
from statistics import mode, mean

class SubjectProfessorSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    subject_name = serializers.CharField()
    professor = serializers.CharField(allow_null=True)
    review = serializers.SerializerMethodField()
    semester = serializers.SerializerMethodField()

    class Meta:
        model = SubjectProfessor
        fields = ('id', 'subject_name', 'professor', 'review', 'semester')


    def validate(self, data):
        if SubjectProfessor.objects.filter(subject_name=data['subject_name'], professor=data['professor']):
            raise CustomException("이미 존재하는 Subject-Professor 입니다.", status.HTTP_409_CONFLICT)
        # create 시의 logic
        return data

    def get_semester(self, obj):
        lectures = Lecture.objects.filter(subject_professor=obj)
        set_year_season = set([(i.year, i.season) for i in lectures])

        data = []
        for i in set_year_season:
            data.append(str(i[0])+"년 "+Lecture.SeasonCode[i[1]])

        return data

    def get_review(self, obj):

        reviews = Review.objects.filter(subject_professor=obj)
        if not reviews:
            return None

        data = {}

        fields = ("homework", "team_activity", "grading", "attendance", "test_count", "rating")
        functions = (mode, mode, mode, mode, mode, mean)

        for field, function in zip(fields, functions):
            data[field] = function([i.__getattribute__(field) for i in reviews])

        data['homework'] = Review.HomeworkCode[data['homework']]
        data['team_activity'] = Review.TeamActivityCode[data['team_activity']]
        data['grading'] = Review.GradingCode[data['grading']]
        data['attendance'] = Review.AttendanceCode[data['attendance']]
        data['test_count'] = str(data['test_count'])

        return data


class LectureSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField()
    professor = serializers.CharField(allow_null=True)
    subject_code = serializers.CharField()
    ####
    year = serializers.IntegerField()
    season = serializers.IntegerField()
    ####
    university = serializers.CharField(required = True, write_only=True)
    college = serializers.CharField(required = False, allow_null=True)
    department = serializers.CharField(required = False, allow_null=True)
    grade = serializers.IntegerField()
    level = serializers.IntegerField()
    credit = serializers.IntegerField()
    category = serializers.IntegerField()
    number = serializers.IntegerField()
    detail = serializers.CharField(allow_null=True)
    language = serializers.CharField()
    ####
    time = serializers.CharField(allow_null=True)
    location = serializers.CharField(allow_null=True)

    class Meta:
        model = Lecture
        fields = ('subject_name', 'subject_code', 'professor',
                  'year', 'season', 'college', 'department', 'grade', 'level', 'credit',
                  'category', 'number', 'detail', 'language',
                  'time', 'location', 'university')

    def validate(self, data):
        university = University.objects.get_or_none(name = data['university'])
        if not university:
            raise CustomException("존재하지 않는 대학입니다.", status.HTTP_400_BAD_REQUEST)
        
        data.pop('university')

        if 'college' in data:
            college_name = data.get('college')
            college = College.objects.get_or_none(name = college_name, university=university)
            if not college:
                raise CustomException("존재하지 않는 단과대입니다.", status.HTTP_400_BAD_REQUEST)

            if 'department' in data:
                department_name = data.get('department')
                department = Department.objects.get_or_none(name = department_name, college = college)
                if not department:
                    raise CustomException("존재하지 않는 학과입니다.", status.HTTP_400_BAD_REQUEST)
            else:
                department = None
        else:
            college = None
            department = None

        data['college'] = college
        data['department'] = department
        
        return data

    def create(self, validated_data):
        subject_professor = SubjectProfessor.objects.get_or_none\
            (subject_name=validated_data['subject_name'], professor=validated_data['professor'])

        if not subject_professor:
            serializer = SubjectProfessorSerializer(
                data={"subject_name": validated_data['subject_name'],
                      "professor": validated_data['professor']})
            serializer.is_valid(raise_exception=True)
            subject_professor = serializer.save()

        validated_data['subject_professor'] = subject_professor
        validated_data.pop('subject_name')
        validated_data.pop('professor')

        lecture = Lecture.objects.create(**validated_data)
        return lecture

    def update(self, instance, validated_data):
        validated_data.pop('subject_name')
        validated_data.pop('professor')
        super().update(instance, validated_data)


class LectureViewSerializer(LectureSerializer):
    id = serializers.IntegerField()
    subject_name = serializers.SerializerMethodField()
    professor = serializers.SerializerMethodField()
    ####
    season = serializers.SerializerMethodField()
    ####
    level = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()
    college = serializers.SerializerMethodField()
    ####

    class Meta:
        model = Lecture
        fields = '__all__'

    def get_subject_name(self, obj):
        return obj.subject_professor.subject_name

    def get_professor(self, obj):
        return obj.subject_professor.professor

    def get_season(self, obj):
        return Lecture.SeasonCode[obj.season]

    def get_level(self, obj):
        return Lecture.LevelCode[obj.level]

    def get_category(self, obj):
        return Lecture.CategoryCode[obj.category]

    def get_department(self, obj):
        if not obj.department:
            return None
        return obj.department.name

    def get_college(self, obj):
        if not obj.college:
            return None
        return obj.college.name



class LectureViewSerializer_Mini(LectureViewSerializer):
    class Meta:
        model = Lecture
        fields = ('id', 'year', 'season')
