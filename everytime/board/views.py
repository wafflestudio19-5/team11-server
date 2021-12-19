from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BoardNameSerializer, BoardSerializer
from university.models import University
from .models import Board

# Create your views here.
class AddBoard(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request):

        serializer = BoardSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        board = serializer.save()
        return Response({"status": "successfully uploaded"}, status=status.HTTP_201_CREATED)

class BoardList(APIView):
    permission_classes = (permissions.AllowAny, )
    def get(self, request):

        if "university" not in request.data:
            return Response({"status": "university is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            university = University.objects.get(name=request.data['university'])
        except ObjectDoesNotExist:
            return Response({"status": "university does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        boards = Board.objects.filter(university=university)
        return Response(BoardNameSerializer(boards, many=True).data, status=status.HTTP_200_OK)

class CustomizedBoardList(APIView):
    permission_classes = (permissions.IsAuthenticated, )
    def get(self, request):

        university = request.user.university
        boards = Board.objects.filter(university=university)
        return Response(BoardNameSerializer(boards, many=True).data, status=status.HTTP_200_OK)

class BoardViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /department/'}, status=status.HTTP_200_OK)