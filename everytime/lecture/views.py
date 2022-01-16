from re import U

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from .filter import filter_lectures

from .serializers import *
from university.models import University
from .models import Lecture

class SubjectProfessorViewSet(viewsets.GenericViewSet):
    serializer_class = LectureSerializer
    permission_classes = (permissions.AllowAny,)  # 테스트용 임시

    # GET /subject_professor/
    def list(self, request):
        subject_professors = SubjectProfessor.objects.filter(professor__isnull=False)
        page = self.paginate_queryset(subject_professors)
        if page is not None:
            serializer = SubjectProfessorSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")

    # GET /subject_professor/{id}
    def retrieve(self, request, pk):
        if not (subject_professor := SubjectProfessor.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "wrong_id", "detail": "SubjectProfessor가 존재하지 않습니다."})

        serializer = SubjectProfessorSerializer(subject_professor, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
        
class SubjectProfessorDetailViewSet(viewsets.GenericViewSet):
    serializer_class = LectureSerializer
    permission_classes = (permissions.AllowAny,)  # 테스트용 임시

    # GET /subject_professor/{subject_professor_id}/lecture/
    def list(self, request, subject_professor_id):
        lectures = Lecture.objects.filter(subject_professor_id=subject_professor_id)

        filter_lectures(lectures, request.query_params)

        page = self.paginate_queryset(lectures)

        if page is not None:
            serializer = LectureViewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")




class LectureViewSet(viewsets.GenericViewSet):
    serializer_class = LectureSerializer
    permission_classes = (permissions.AllowAny,)  # 테스트용 임시

    # GET /lecture/
    def list(self, request):

        lectures = filter_lectures(Lecture.objects.all(), request.query_params)

        page = self.paginate_queryset(lectures)
        if page is not None:
            serializer = LectureViewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")


    # POST /lecture/
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        lecture = serializer.save()

        return Response(status=status.HTTP_200_OK, data=LectureViewSerializer(lecture).data)

    # PUT /lecture/
    def put(self, request):

        required = {}
        for i in ['subject_name', 'subject_code', 'professor', 'year', 'season', 'number']:
            if i not in request.data:
                required[i] = ["This field is required."]

        if required:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=required)


        #subject_professor를 불러옴
        subject_name = request.data['subject_name']
        professor = request.data['professor'] if request.data['professor'] else None

        subject_professor = SubjectProfessor.objects.get_or_none(subject_name=subject_name, professor=professor)
        if not subject_professor:
            return Response(status=status.HTTP_404_NOT_FOUND, data="존재하지 않는 Subject-Professor입니다. ")

        #lecture를 불러옴
        # lecture에서 subject_code만 다른 경우 있음 (김건희의 고급인공지능)
        lecture = Lecture.objects.get_or_none(subject_professor=subject_professor,
                                              year=request.data['year'],
                                              season=request.data['season'],
                                              number=request.data['number'],
                                              subject_code=request.data['subject_code'])

        if not lecture:
            return Response(status=status.HTTP_404_NOT_FOUND, data="존재하지 않는 Lecture입니다. ")

        serializer = self.get_serializer(lecture, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(lecture, serializer.validated_data)

        return Response(status=status.HTTP_200_OK, data=LectureViewSerializer(lecture).data)


