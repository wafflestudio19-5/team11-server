from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Department
from university.models import University
from .serializers import DepartmentSerializer


# Create your views here.
class AddDepartment(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request):

        serializer = DepartmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        department = serializer.save()
        return Response({"status": "successfully uploaded"}, status=status.HTTP_201_CREATED)

class DepartmentViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /department/'}, status=status.HTTP_200_OK)