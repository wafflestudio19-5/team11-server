from re import U
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import *
from university.models import University
from .models import Board

# Create your views here.
class BoardViewSet(viewsets.GenericViewSet):
    serializer_class = BoardSerializer
    permission_classes = (permissions.AllowAny, ) # 테스트용 임시

    # GET /board/?
    def list(self, request):
        query = request.query_params
        keyword = query.get('search')
        
        if keyword == None:
            boards = Board.objects.all()
            return Response(status=status.HTTP_200_OK, data={ "boards" : BoardGetSeriallizer(boards, many = True).data})
        else:
            filtered_boards = Board.objects.filter(name__icontains = keyword)
            if len(filtered_boards) == 0:
                return Response(status = status.HTTP_404_NOT_FOUND, data = { "error" : "result_not_found", "detail" : "검색 결과가 없습니다."})
            
            return Response(status=status.HTTP_200_OK, data={ "boards" : BoardFilteredSerializer(filtered_boards, many = True).data})

    # POST /board/
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = BoardNameSerializer(serializer.instance)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # PUT /board/{board_id}/
    def update(self, request, pk):
        if not (board := Board.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_id", "detail" : "게시판이 존재하지 않습니다."})

        serializer = self.get_serializer(data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(board, serializer.validated_data)

        serializer = BoardNameSerializer(board)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # DELETE /board/ 
    def destroy(self, request, pk):
        return Response(status=status.HTTP_200_OK, data='DELETE /board/')

    # GET /board/{board_id}/?offset=[offset]&?limit=[limit]
    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_200_OK, data='GET /board/board_id/?offset=[offset]&?limit=[limit]')
