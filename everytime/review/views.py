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


class ReviewViewSet(viewsets.GenericViewSet):
    serializer_class = ReviewCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    # POST /subject_professor/{subject_professor}/review/
    def create(self, request, subject_professor_id):
        if not (subject_professor := SubjectProfessor.objects.get_or_none(id=subject_professor_id)):
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"error": "wrong_board_id", "detail": "SubjectProfessor가 존재하지 않습니다."})


        data = request.data.copy()
        data['subject_professor'] = subject_professor_id
        serializer = ReviewCreateSerializer(data=data, context={'request': request})
        valid = serializer.is_valid(raise_exception=True)
        review = serializer.save()
        print(review)
        #review = None
        return Response(status=status.HTTP_200_OK, data=ReviewViewSerializer(review).data)

    # GET /subject_professor/{subject_professor}/review/
    def list(self, request, subject_professor_id):
        if not (subject_professor := SubjectProfessor.objects.get_or_none(id=subject_professor_id)):
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"error": "wrong_board_id", "detail": "SubjectProfessor가 존재하지 않습니다."})

        reviews = Review.objects.filter(subject_professor=subject_professor)
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewViewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")




