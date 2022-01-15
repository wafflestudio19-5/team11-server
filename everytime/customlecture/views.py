from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from operator import itemgetter, attrgetter, methodcaller
from django.db.models.query import QuerySet
import datetime

from .serializers import *
from lecture.models import *
from university.models import University
from board.models import Board
#from .models import Article
import requests


class CustomLectureViewSet(viewsets.GenericViewSet):
    serializer_class = CustomLectureCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # POST /schedule/{id}/custom_lecture/
    def create(self, request, schedule_id):
        if schedule_id == 'default':
            schedule = Schedule.get_default_schedule(request.user)
        else:
            schedule = Schedule.objects.get_or_none(id=schedule_id)

        data = request.data

        if 'lecture' in data:

            serializer = CustomLectureCreateSerializer(data=data, context={'request': request, 'schedule': schedule})
            valid = serializer.is_valid(raise_exception=True)
            custom_lecture = serializer.save()

        else:
            serializer = CustomLectureCreateSerializer_Custom(data=data, context={'request': request, 'schedule': schedule})
            valid = serializer.is_valid(raise_exception=True)
            custom_lecture = serializer.save()

        return Response(status=status.HTTP_200_OK, data=CustomLectureViewSerializer(custom_lecture).data)

    # GET /schedule/{id}/custom_lecture/

    def list(self, request, schedule_id):

        if schedule_id == 'default':
            schedule = Schedule.get_default_schedule(request.user)
        else:
            schedule = Schedule.objects.get_or_none(id=schedule_id)

        if not schedule:
            return Response(status=status.HTTP_404_NOT_FOUND, data="존재하지 않는 시간표입니다.")

        schedule.last_visit = datetime.datetime.now()
        schedule.save()

        custom_lecture = CustomLecture.objects.filter(schedule=schedule)

        page = self.paginate_queryset(custom_lecture)
        if page is not None:
            serializer = CustomLectureViewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")

    @classmethod
    def get_schedule_custom_lecture(cls, schedule_id, custom_lecture_id, user):
        if schedule_id == 'default':
            schedule = Schedule.get_default_schedule(user)
        else:
            schedule = Schedule.objects.get_or_none(id=schedule_id)

        if not schedule:
            return "해당되는 시간표가 없습니다", None

        custom_lecture = CustomLecture.objects.get_or_none(id=custom_lecture_id)

        if not custom_lecture:
            return "해당되는 강의가 없습니다", None

        if custom_lecture.schedule != schedule:
            return "시간표에 속하지 않는 강의입니다.", None

        return schedule, custom_lecture

    # GET /schedule/{id}/custom_lecture/{id}

    def retrieve(self, request, schedule_id, pk):
        schedule, custom_lecture = self.get_schedule_custom_lecture(schedule_id, pk, request.user)
        if not custom_lecture:
            return Response(status=status.HTTP_404_NOT_FOUND, data=schedule)

        print(custom_lecture.get_time())

        return Response(status=status.HTTP_200_OK, data=CustomLectureViewSerializer(custom_lecture).data)

    # PUT /schedule/{id}/custom_lecture/{id}

    def put(self, request, schedule_id, pk):
        schedule, custom_lecture = self.get_schedule_custom_lecture(schedule_id, pk, request.user)
        if not custom_lecture:
            return Response(status=status.HTTP_404_NOT_FOUND, data=schedule)


        serializer = CustomLecturePutSerializer(custom_lecture, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(custom_lecture, serializer.validated_data)

        return Response(status=status.HTTP_200_OK, data=CustomLectureViewSerializer(custom_lecture).data)
        ##return Response(status=status.HTTP_200_OK, data="성공적으로 삭제되었습니다")

    # DELETE /schedule/{id}/custom_lecture/{id}

    def delete(self, request, schedule_id, pk):
        schedule, custom_lecture = self.get_schedule_custom_lecture(schedule_id, pk, request.user)
        if not custom_lecture:
            return Response(status=status.HTTP_404_NOT_FOUND, data=schedule)

        custom_lecture.delete()
        return Response(status=status.HTTP_200_OK, data="성공적으로 삭제되었습니다")



