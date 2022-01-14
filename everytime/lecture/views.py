from re import U

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from university.models import University
from .models import Lecture

class SubjectProfessorViewSet(viewsets.GenericViewSet):
    serializer_class = LectureSerializer
    permission_classes = (permissions.AllowAny,)  # 테스트용 임시

    # GET /subject_professor/
    def list(self, request):
        subject_professors = SubjectProfessor.objects.all()
        page = self.paginate_queryset(subject_professors)
        if page is not None:
            serializer = SubjectProfessorSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")
        
class SubjectProfessorDetailViewSet(viewsets.GenericViewSet):
    serializer_class = LectureSerializer
    permission_classes = (permissions.AllowAny,)  # 테스트용 임시

    # GET /subject_professor/{subject_professor_id}/lecture/
    def list(self, request, subject_professor_id):
        lectures = Lecture.objects.filter(subject_professor_id=subject_professor_id)
        page = self.paginate_queryset(lectures)

        if page is not None:
            serializer = LectureViewSerializer_Mini(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")

class LectureViewSet(viewsets.GenericViewSet):
    serializer_class = LectureSerializer
    permission_classes = (permissions.AllowAny,)  # 테스트용 임시

    # GET /lecture/
    def list(self, request):

        query = request.query_params

        lectures = Lecture.objects.all()

        if 'subject' in query:
            subject = query.get('subject')
            if not subject:
                lectures = Lecture.objects.none()
            else:
                q = Q()
                keywords = set(subject.split(' '))
                for k in keywords:
                    q &= Q(subject_professor__subject_name__icontains=k)
                lectures = lectures.filter(q)

        if 'subject_code' in query:
            subject_code = query.get('subject_code')
            if not subject_code:
                lectures = Lecture.objects.none()
            else:
                lectures = lectures.filter(subject_code=subject_code)

        if 'professor' in query:
            professor = query.get('professor')
            if not professor:
                lectures = Lecture.objects.none()
            else:
                lectures = lectures.filter(subject_professor__professor__icontains=professor)

        if 'year' in query:
            try:
                year = int(query.get('year'))
                lectures = lectures.filter(year=year)
            except Exception:
                lectures = Lecture.objects.none()

        if 'season' in query:
            try:
                season = int(query.get('season'))
                lectures = lectures.filter(season=season)
            except Exception:
                lectures = Lecture.objects.none()

        if 'department' in query:
            department = query.get('department').split(' ')
            lectures = lectures.filter(department__in=department)

        if 'grade' in query:
            try:
                grade = [int(i) for i in query.get('grade').split(' ')]
                lectures = lectures.filter(grade__in=grade)
            except Exception:
                lectures = Lecture.objects.none()

        if 'level' in query:
            try:
                level = [int(i) for i in query.get('level').split(' ')]
                lectures = lectures.filter(level__in=level)
            except Exception:
                lectures = Lecture.objects.none()

        if 'credit' in query:
            try:
                credit = [int(i) for i in query.get('credit').split(' ')]
                lectures = lectures.filter(credit__in=credit)
            except Exception:
                lectures = Lecture.objects.none()

        if 'category' in query:
            try:
                category = [int(i) for i in query.get('category').split(' ')]
                lectures = lectures.filter(category__in=category)
            except Exception:
                lectures = Lecture.objects.none()

        if 'language' in query:
            language = query.get('language').split(' ')
            lectures = lectures.filter(language__in=language)

        if 'location' in query:
            locations = query.get('location').split(' ')
            if not locations:
                lectures = Lecture.objects.none()
            else:
                q = Q()
                for k in locations:
                    q &= Q(location__icontains=k+"-")
                lectures = lectures.filter(q)


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

        subject_professor = SubjectProfessor.objects.get_or_none(subject_name=request.data['subject_name'], professor=request.data['professor'])
        if not subject_professor:
            return Response(status=status.HTTP_404_NOT_FOUND, data="존재하지 않는 Subject-Professor입니다. ")
        lecture = Lecture.objects.get_or_none(subject_professor=subject_professor, year=request.data['year'],
                                              season=request.data['season'], number=request.data['number'],
                                              subject_code=request.data['subject_code'])

        #lecture에서 subject_code만 다른 경우 있음 (김건희의 고급인공지능)

        if not lecture:
            return Response(status=status.HTTP_404_NOT_FOUND, data="존재하지 않는 Lecture입니다. ")

        serializer = self.get_serializer(lecture, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(lecture, serializer.validated_data)

        return Response(status=status.HTTP_200_OK, data=LectureViewSerializer(lecture).data)


    '''
    # PUT /board/{board_id}/
    def update(self, request, pk):
        if not (board := Board.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "wrong_id", "detail": "게시판이 존재하지 않습니다."})

        serializer = self.get_serializer(board, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(board, serializer.validated_data)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # GET /board/{board_id}/
    def retrieve(self, request, pk):
        if not (board := Board.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "wrong_id", "detail": "게시판이 존재하지 않습니다."})

        serializer = self.get_serializer(board)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # DELETE /board/
    def destroy(self, request, pk):

        if not (board := Board.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "wrong_id", "detail": "게시판이 존재하지 않습니다."})

        if not request.user.is_superuser and request.user != board.manager:
            return Response(status=status.HTTP_401_UNAUTHORIZED,
                            data={"error": "wrong_user", "detail": "게시판 관리자만 접근 가능합니다."})

        board = Board.objects.get(id=pk)
        board.delete()
        return Response(status=status.HTTP_200_OK, data={"success": True})
    '''
