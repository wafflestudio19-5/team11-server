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

    # GET /board/
    # GET /board/?search=[keyword]
    def list(self, request):
        query = request.query_params
        keyword = query.get('search')
        
        if keyword == None:
            boards = Board.objects.all()
            return Response(status=status.HTTP_200_OK, data={ "boards" : BoardGetSeriallizer(boards, many = True, context={'request': request}).data})
        else:
            filtered_boards = Board.objects.filter(name__icontains = keyword)
            if len(filtered_boards) == 0:
                return Response(status = status.HTTP_404_NOT_FOUND, data = { "error" : "result_not_found", "detail" : "검색 결과가 없습니다."})
            
            return Response(status=status.HTTP_200_OK, data={ "boards" : BoardGetSeriallizer(filtered_boards, many = True, context={'request': request}).data})

    # POST /board/
    def create(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        serializer = BoardNameSerializer(serializer.instance, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # PUT /board/{board_id}/
    def update(self, request, pk):
        if not (board := Board.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_id", "detail" : "게시판이 존재하지 않습니다."})

        serializer = self.get_serializer(board, data=request.data, context={'request': request}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.update(board, serializer.validated_data)

        serializer = BoardNameSerializer(board, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    #GET /board/{board_id}/
    def retrieve(self, request, pk):
        if not (board := Board.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_id", "detail" : "게시판이 존재하지 않습니다."})
        
        serializer = BoardNameSerializer(board, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    # DELETE /board/ 
    def destroy(self, request, pk):


        if not (board := Board.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "error":"wrong_id", "detail" : "게시판이 존재하지 않습니다."})

        if not request.user.is_superuser and request.user != board.manager :
            return Response(status=status.HTTP_401_UNAUTHORIZED, data = {"error" : "wrong_user", "detail" : "게시판 관리자만 접근 가능합니다."})

        board = Board.objects.get(id =pk)
        board.delete()
        return Response(status=status.HTTP_200_OK, data={"success" : True})

class UserBoardViewSet(viewsets.GenericViewSet):
    serializer_class = BoardSerializer
    permission_classes = (permissions.IsAuthenticated, )

    # PUT /board_favorite/{board_id}/
    def update(self, request, pk):
        if not (board := Board.objects.get_or_none(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={"error": "wrong_id", "detail": "게시판이 존재하지 않습니다."})

        user_board = UserBoard.objects.get_or_none(user=request.user, board=board)

        if user_board:
            user_board.favorite = not user_board.favorite
            user_board.save()
        else:
            UserBoard.objects.create(user=request.user, board=board)

        return Response(status=status.HTTP_200_OK, data={"board": board.id, "favorite": user_board.favorite})

    # GET /board_favorite/
    # GET /board_favorite/?search=[keyword]
    def list(self, request):

        query = request.query_params
        keyword = query.get('search')
        id_only = query.get('id_only')

        boards = Board.objects.filter(user_board__user=request.user, user_board__favorite=True)

        if keyword is not None:
            boards = boards.filter(name__icontains=keyword)

        if len(boards) == 0:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data={"error": "result_not_found", "detail": "검색 결과가 없습니다."})

        if id_only:
            return Response(status=status.HTTP_200_OK,
                            data={"boards": sorted(boards.values_list('id', flat=True))})

        return Response(status=status.HTTP_200_OK, data={
            "boards": BoardGetSeriallizer(boards, many=True, context={'request': request}).data})

