from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import IntegrityError
from user.serializers import UserCreateSerializer, UserLoginSerializer
from user.models import User

# Create your views here.
class UserSignUpView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, jwt_token = serializer.save()
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT, data='중복되는 계정입니다. 중복확인 제대로 했는지 확인해주세요.')

        return Response({'user': user.user_id, 'token': jwt_token}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
    
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        return Response({'success': True, 'token': token}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /user/'}, status=status.HTTP_200_OK)

class UserCheckIDView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        data = request.query_params
        user_id = data.get('user_id')
        if not user_id:
            return Response({'아이디를 입력해주세요.'}, status = status.HTTP_400_BAD_REQUEST)
        for user in queryset:
            if user.user_id == user_id:
                return Response({"check" : "False", "detail" : '이미 사용중인 아이디입니다.'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"check" : "True", "detail": '사용 가능한 아이디입니다.'}, status = status.HTTP_200_OK)

class UserCheckUsernameView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        data = request.query_params
        nickname = data.get('nickname')
        if not nickname:
            return Response({'닉네임을 입력해주세요.'}, status = status.HTTP_400_BAD_REQUEST)
        for user in queryset:
            if user.nickname == nickname:
                return Response({"check" : "False", "detail" : "이미 사용중인 닉네임입니다."}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"check" : "True", "detail" : "사용 가능한 닉네임입니다."}, status = status.HTTP_200_OK)

class UserCheckEmailView(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        data = request.query_params
        email = data.get('email')
        if not email:
            return Response({'이메일를 입력해주세요.'}, status = status.HTTP_400_BAD_REQUEST)
        for user in queryset:
            if user.email == email:
                return Response({"check" : "False" , "detail" : '이미 사용중인 이메일입니다.'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"check" : "True", "detail" : "사용 가능한 이메일입니다."}, status = status.HTTP_200_OK)