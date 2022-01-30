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
from lecture.serializers import LectureViewSerializer
from lecture.filter import filter_lectures


class ScheduleViewSet(viewsets.GenericViewSet):
    serializer_class = ScheduleCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # POST /schedule/
    def create(self, request):
        data = request.data.copy()

        serializer = ScheduleCreateSerializer(data=data, context={'request': request})
        valid = serializer.is_valid(raise_exception=True)
        schedule = serializer.save()

        return Response(status=status.HTTP_201_CREATED, data=ScheduleViewSerializer(schedule,  context={'request': request}).data)

    # GET /schedule/
    def list(self, request):
        schedules = self.get_queryset().filter(user=request.user)

        page = self.paginate_queryset(schedules)
        if page is not None:
            serializer = ScheduleViewSerializer(page, context={'request': request}, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")

    def get_queryset(self):
        queryset = Schedule.objects.all()
        return queryset


    # GET /schedule/{id}/
    def retrieve(self, request, pk):
        if pk == 'default':
            schedule = Schedule.get_default_schedule(request.user)
        else:
            schedule = Schedule.objects.get_or_none(id=pk)

        if not schedule:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "wrong_id", "detail": "시간표가 존재하지 않습니다."})

        #schedule.last_visit = datetime.datetime.now()
        #schedule.save()
        serializer = ScheduleViewSerializer(schedule, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, pk): # 정상적으로 작동하는지 확인해볼 것
        if pk == 'default':
            schedule = Schedule.get_default_schedule(request.user)
        else:
            schedule = Schedule.objects.get_or_none(id=pk)

        if not schedule:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "wrong_id", "detail": "시간표가 존재하지 않습니다."})

        #print(schedule, request.data)

        serializer = ScheduleNameSerializer(schedule, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.update(schedule, serializer.validated_data)

        return Response(status=status.HTTP_200_OK, data=ScheduleViewSerializer(schedule,  context={'request': request}).data)

    def delete(self, request, pk): # schedule = None일 경우 내가 볼때 문제가 발생한다. 체크해보자.
        if pk == 'default':
            schedule = Schedule.get_default_schedule(request.user)
        else:
            schedule = Schedule.objects.get_or_none(id=pk)

        if not schedule:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "wrong_id", "detail": "시간표가 존재하지 않습니다."})

        if schedule.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN, data={"error": "forbidden", "detail": "삭제 권한이 없습니다."})

        schedule.delete()
        return Response(status=status.HTTP_200_OK, data="성공적으로 지워졌습니다.")


class ScheduleLectureViewSet(viewsets.GenericViewSet):
    def list(self, request, schedule_id):
        if schedule_id == 'default':
            schedule = Schedule.get_default_schedule(request.user)
        else:
            schedule = Schedule.objects.get_or_none(id=schedule_id)

        if not schedule:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "wrong_id", "detail": "시간표가 존재하지 않습니다."})

        query = request.query_params

        lectures = self.get_queryset()
        lectures = filter_lectures(lectures.filter(year=schedule.year, season=schedule.season), query)

        page = self.paginate_queryset(lectures)
        if page is not None:
            serializer = LectureViewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")

    def get_queryset(self):
        queryset = Lecture.objects.all()
        return queryset



