from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from operator import itemgetter, attrgetter, methodcaller
from django.db.models.query import QuerySet

from .serializers import *
from lecture.models import *
from university.models import University
from board.models import Board
#from .models import Article
import requests


class ScheduleViewSet(viewsets.GenericViewSet):
    serializer_class = ScheduleCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # POST /schedule/
    def create(self, request):
        data = request.data

        serializer = ScheduleCreateSerializer(data=data, context={'request': request})
        valid = serializer.is_valid(raise_exception=True)
        schedule = serializer.save()
        #print(review)
        #review = None
        return Response(status=status.HTTP_200_OK, data=ScheduleViewSerializer(schedule).data)

    # GET /schedule/
    def list(self, request):

        schedules = Schedule.objects.filter(user=request.user)

        page = self.paginate_queryset(schedules)
        if page is not None:
            serializer = ScheduleViewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")

    def retrieve(self, request, pk):
        if not (schedule := Schedule.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "wrong_id", "detail": "시간표가 존재하지 않습니다."})

        serializer = ScheduleViewSerializer(schedule, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)



