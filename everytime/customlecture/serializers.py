from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers, status
from django.db import transaction
from django.utils import timezone

from article.models import Article
from comment.models import Comment
from .models import *
from comment.serializers import CommentSerializer
from functools import reduce
from django.db.models import Q
from common.custom_exception import CustomException

class CustomLectureCreateSerializer(serializers.ModelSerializer): # lecture_id 기반 custom_lecture

    lecture = serializers.IntegerField()
    memo = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = CustomLecture
        fields = ('lecture', 'memo')

    def validate(self, data):
        user = self.context['request'].user

        schedule = self.context['schedule']

        if not schedule:
            raise CustomException("존재하지 않는 시간표입니다. ", status.HTTP_404_NOT_FOUND)

        lecture = Lecture.objects.get_or_none(id=data['lecture'], year=schedule.year, season=schedule.season)
        if not lecture:
            raise CustomException("존재하지 않는 강의입니다. ", status.HTTP_404_NOT_FOUND)

        if schedule.user != user:
            raise CustomException("편집 권한이 없습니다. ", status.HTTP_403_FORBIDDEN)

        custom_lectures = CustomLecture.objects.filter(schedule=schedule)
        if custom_lectures:
            current_time = reduce(lambda s1, s2: s1.union(s2), [i.get_time() for i in custom_lectures])
        else:
            current_time = set()
        new_time = CustomLecture.string_to_time_set(lecture.time)

        for nt in new_time:
            for ct in current_time:
                if nt[0] != ct[0]:
                    continue
                if ct[2] <= nt[1] or nt[2] <= ct[1]:
                    continue
                raise CustomException("기존의 강의와 겹칩니다. ", status.HTTP_409_CONFLICT)


        return data

    def create(self, validated_data):
        #validated_data['user'] = self.context['request'].user
        validated_data['schedule'] = self.context['schedule']

        lecture = Lecture.objects.get(id=validated_data['lecture'])
        validated_data['lecture'] = lecture

        validated_data['professor'] = lecture.subject_professor.professor
        validated_data['time'] = lecture.time
        validated_data['location'] = lecture.location
        validated_data['nickname'] = lecture.subject_professor.subject_name

        return CustomLecture.objects.create(**validated_data)

class CustomLectureCreateSerializer_Custom(serializers.ModelSerializer): # lecture에 없는 수업 생성

    nickname = serializers.CharField(max_length=100)
    professor = serializers.CharField(max_length=100, required=False, allow_null=True, allow_blank=True)
    time_location = serializers.ListField()
    memo = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = CustomLecture
        fields = ('nickname', 'professor', 'time', 'location', 'memo', 'time_location')

    def validate(self, data):
        user = self.context['request'].user
        schedule = self.context['schedule']

        if not schedule:
            raise CustomException("존재하지 않는 시간표입니다. ", status.HTTP_404_NOT_FOUND)

        if schedule.user != user:
            raise CustomException("편집 권한이 없습니다. ", status.HTTP_403_FORBIDDEN)

        custom_lectures = CustomLecture.objects.filter(schedule=schedule)
        if custom_lectures:
            current_time = reduce(lambda s1, s2: s1.union(s2), [i.get_time() for i in custom_lectures])
        else:
            current_time = set()

        #time_location = data['time_location']
        #for i in range(1, len(time_location)//2 + 1):
        for i in data['time_location']:
            time = i['time']
            #time = time_location['time'+str(i)]
            # location = time_location['location'+str(i)]

            try:
                new_time = CustomLecture.string_to_time_set(time)
            except Exception:
                raise CustomException("time의 형식이 잘못되었습니다. ", status.HTTP_400_BAD_REQUEST)

            for nt in new_time:
                for ct in current_time:
                    if nt[0] != ct[0]:
                        continue
                    if ct[2] <= nt[1] or nt[2] <= ct[1]:
                        continue
                    raise CustomException("기존의 강의와 겹칩니다. ", status.HTTP_409_CONFLICT)
                current_time.add(nt)

        return data

    def create(self, validated_data):
        #validated_data['user'] = self.context['request'].user
        validated_data['schedule'] = self.context['schedule']

        time_location = validated_data.pop('time_location')
        validated_data['time'] = validated_data['location'] = ""

        for i in time_location:
            time = i['time']
            location = i['location']
            if not location:
                location = ""
            #time = time_location['time'+str(i)]
            #location = time_location['location'+str(i)]

            validated_data['time'] += (time + '/')
            validated_data['location'] += (location + '\t')

        validated_data['time'] = validated_data['time'][:-1]
        validated_data['location'] = validated_data['location'][:-1]

        return CustomLecture.objects.create(**validated_data)

class CustomLecturePutSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    memo = serializers.CharField(max_length=200, required=False, allow_blank=True, allow_null=True)
    time_location = serializers.ListField(required=False)

    class Meta:
        model = CustomLecture
        fields = ('nickname', 'memo', 'time_location')

    def validate(self, data):

        if "time_location" in data:
            custom_lecture = self.context['custom_lecture']

            custom_lectures = CustomLecture.objects.filter(schedule=custom_lecture.schedule)
            custom_lectures = custom_lectures.filter(~Q(id=custom_lecture.id))
            if custom_lectures:
                current_time = reduce(lambda s1, s2: s1.union(s2), [i.get_time() for i in custom_lectures])
            else:
                current_time = set()

            for i in data['time_location']:
                time = i['time']

                try:
                    new_time = CustomLecture.string_to_time_set(time)
                except Exception:
                    raise CustomException("time의 형식이 잘못되었습니다. ", status.HTTP_400_BAD_REQUEST)

                for nt in new_time:
                    for ct in current_time:
                        if nt[0] != ct[0]:
                            continue
                        if ct[2] <= nt[1] or nt[2] <= ct[1]:
                            continue
                        raise CustomException("기존의 강의와 겹칩니다. ", status.HTTP_409_CONFLICT)
                    current_time.add(nt)
        
        return data
        
    def update(self, instance, validated_data):
        if "time_location" in validated_data:
            if instance.lecture:
                raise CustomException("시공간 정보를 바꿀 수 없는 강의입니다. ", status.HTTP_400_BAD_REQUEST)
            time_location = validated_data.pop('time_location')
            validated_data['time'] = validated_data['location'] = ""

            for i in time_location:
                time = i['time']
                location = i['location']
                if not location:
                    location = ""
                #time = time_location['time'+str(i)]
                #location = time_location['location'+str(i)]

                validated_data['time'] += (time + '/')
                validated_data['location'] += (location + '\t')

            validated_data['time'] = validated_data['time'][:-1]
            validated_data['location'] = validated_data['location'][:-1]

        if 'nickname' in validated_data:
            if not validated_data['nickname']:
                if not instance.lecture:
                    raise CustomException("수업명을 입력해 주세요. ", status.HTTP_400_BAD_REQUEST)
                else:
                    validated_data['nickname'] = instance.lecture.subject_professor.subject_name
        
        result = super().update(instance, validated_data)
        instance.save()
        return result

class CustomLectureViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    lecture = serializers.SerializerMethodField()
    nickname = serializers.CharField()
    professor = serializers.CharField()
    time = serializers.CharField()
    location = serializers.CharField()
    memo = serializers.CharField()
    time_location = serializers.SerializerMethodField()
    subject_professor = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ('id', 'subject_professor', 'lecture', 'nickname', 'professor', 'time', 'location', 'memo', 'time_location', 'url')

    def get_subject_professor(self, obj):
        if not obj.lecture:
            return 0
        return obj.lecture.subject_professor.id

    def get_url(self, obj):
        if not obj.lecture:
            return ""
        return ("https://sugang.snu.ac.kr/sugang/cc/cc103.action?openSchyy="
                + str(obj.lecture.year)
                + "&openShtmFg=U00020000"
                + str(obj.lecture.season)
                + "&openDetaShtmFg=U000300001&sbjtCd=" 
                + obj.lecture.subject_code + "&ltNo="
                + str(obj.lecture.number).zfill(3)
                + "&sbjtSubhCd=000"
                )


    def get_lecture(self, obj):
        if not obj.lecture:
            return None
        return obj.lecture.id

    def get_time_location(self, obj):
        dict = {}
        times, locations = obj.time, obj.location

        time_code, locations_code = '/', '/'
        if not obj.lecture:
            locations_code = '\t'

        if times:
            times = obj.time.split(time_code)
        if locations:
            locations = obj.location.split(locations_code)

        # 시간이 None
        if not times:
            return None

        # 공간이 None
        # time과 location의 / 갯수가 일치하지 않음
        if not locations or len(times) != len(locations):
            for time in times:
                if time not in dict:
                    dict[time] = set()
                dict[time].add(obj.location)

        # time과 location의 / 갯수가 일치함
        else:
            for time, location in zip(times, locations):
                if time not in dict:
                    dict[time] = set()
                dict[time].add(location)

        data = []

        for time in dict:

            weekdays, clock = time.split('(')[0], time.split('(')[1][:-1]
            start, end = clock.split('~')

            dict[time] -= {None}

            sub_data = {'time': weekdays + "(" + start + "~" + end + ")", 'location': None if not dict[time] else dict[time]}
            data.append(sub_data)

        return data



