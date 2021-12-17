from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UniversityViewSerializer, UniversitySerializer
from .models import University

# Create your views here.
class UniversityList(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request):
        serializer = UniversityViewSerializer
        return Response(serializer(University.objects.all(), many=True).data, status=status.HTTP_200_OK)


class AddUniversity(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request):
        serializer = UniversitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        university = serializer.save()
        return Response({"status": "successfully uploaded"}, status=status.HTTP_201_CREATED)

class UniversityViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /universitry/'}, status=status.HTTP_200_OK)