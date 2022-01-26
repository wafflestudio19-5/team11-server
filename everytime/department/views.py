from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Department, College
from university.models import University
from .serializers import DepartmentCreateSerializer, CollegeCreateSerializer, DepartmentSerializer, CollegeSerializer


# Create your views here.
class DepartmentViewSet(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request):

        serializer = DepartmentCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        department = serializer.save()
        return Response(data = DepartmentSerializer(department).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        data = request.query_params
        if not data.get('college'):
            return Response({'error' : 'college field is required'}, status=status.HTTP_400_BAD_REQUEST)
        college = College.objects.get_or_none(name = data['college'])
        if not college:
            return Response({"error": "단과대가 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset().filter(college = college)
        
        return Response({'college' : data['college'], 'departments' : DepartmentSerializer(queryset, many=True).data}, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = Department.objects.all()
        return queryset

class CollegeViewSet(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request):

        serializer = CollegeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        college = serializer.save()
        return Response(data = CollegeSerializer(college).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        data = request.query_params
        if not data.get('university'):
            return Response({'error' : 'university field is required'}, status=status.HTTP_400_BAD_REQUEST)
        university = University.objects.get_or_none(name = data['university'])
        if not university:
            return Response({"error": "대학이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        queryset = self.get_queryset().filter(university=university)
        
        return Response({'university' : data['university'], 'colleges' : DepartmentSerializer(queryset, many=True).data}, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = College.objects.all()
        return queryset