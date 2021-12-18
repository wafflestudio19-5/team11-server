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
        
    def post(self, request):
        if request.user.is_anonymous:
            pass # test용으로 임시 설정
            #return Response({"error" : "forbidden", "detail" : "관리자만 사용가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        serializer = UniversitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success" : "True"}, status=status.HTTP_201_CREATED)

class UniversityViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /universitry/'}, status=status.HTTP_200_OK)