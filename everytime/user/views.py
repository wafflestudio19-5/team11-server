from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth import authenticate
from django.db import IntegrityError
from user.serializers import UserCreateSerializer, UserLoginSerializer, UserNotificationSerializer
from user.models import User, UserNotification
from django.contrib.auth.models import update_last_login
from django.http.response import Http404
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from rest_framework_jwt.views import VerifyJSONWebTokenSerializer

from common.fcm_notification import send_push
from article.views import ArticleViewSet

import logging
logger = logging.getLogger('django')

# Create your views here.
class UserSignUpView(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        try:
            validate_password(request.data.get('password'), user=request.user)
            user, jwt_token = serializer.save()
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT, data='중복되는 계정입니다. 중복확인 제대로 했는지 확인해주세요.')
        except ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='형식에 맞지 않은 비밀번호입니다. 형식을 맞춰주세요.')

        return Response({'user': user.user_id, 'token': jwt_token}, status=status.HTTP_201_CREATED)

class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = UserLoginSerializer

    def post(self, request):
        # 기본 login 시도
        serializer = UserLoginSerializer(data=request.data)
        try :
            serializer.is_valid(raise_exception=True)
            token = serializer.validated_data['token']
        except Exception as v:
            print(v)
            # validation 실패 시, token으로 login
            try:
                # HTTP Header에서 token 가져온 후 Verify, token 정보로 user 가져옴.
                token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
                data = {'token': token}
                valid_data = VerifyJSONWebTokenSerializer().validate(data)
                user = valid_data['user']
                update_last_login(None, user)
            except Exception as v:
                print(v)
                logger.debug(v)
                return Response({'error': "field_error", 'detail': "이메일 또는 비밀번호가 잘못되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'success': True, 'token': token}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def list(self, request, pk=None):
        user = request.user
        
        try:
            fcm_token = user.fcm_token
            send_push("test", user, fcm_token)
        except Exception as e:
            logger.debug(e)

        serializer = UserCreateSerializer(user, context={'request': request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)
        # return Response(
        #     {
        #         "user_id" : user.user_id,
        #         "name" : user.name,
        #         "email" : user.email,
        #         "admission_year" : user.admission_year,
        #         "nickname" : user.nickname,
        #         "university" : user.university.name
        #     }
        #     ,status=status.HTTP_200_OK)

class UserDeleteViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserCreateSerializer

    def delete(self, request):
        user = request.user
        data = request.data.copy()
        data['is_active'] = False
        word = data.get('password')
        if word == None:
            return Response({"error" : "wrong_password", "detail" : "비밀번호를 입력해주세요."}, status= status.HTTP_400_BAD_REQUEST)
        boolean = authenticate(email=user.email, password=word)
        if boolean is None:
            return Response({"error" : "wrong_password", "detail" : "계정 비밀번호가 올바르지 않습니다."}, status= status.HTTP_400_BAD_REQUEST)
        user.is_active = False
        user.save()
        return Response({"success" : True}, status = status.HTTP_200_OK)

    def list(self, request, pk=None):
        password = request.query_params.get('password')
        return Response({"detail" : password}, status = status.HTTP_200_OK)

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
                return Response({"check" : False, "detail" : '이미 사용중인 아이디입니다.'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"check" : True, "detail": '사용 가능한 아이디입니다.'}, status = status.HTTP_200_OK)

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
                return Response({"check" : False, "detail" : "이미 사용중인 닉네임입니다."}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"check" : True, "detail" : "사용 가능한 닉네임입니다."}, status = status.HTTP_200_OK)

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
                return Response({"check" : False, "detail" : '이미 사용중인 이메일입니다.'}, status = status.HTTP_400_BAD_REQUEST)
        return Response({"check" : True, "detail" : "사용 가능한 이메일입니다."}, status = status.HTTP_200_OK)

class UserUpdateEmailView(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserCreateSerializer
    def put(self, request, pk = None):
        user = request.user
        data = request.data.copy()
        if data.get('email') == None:
            return Response({"error" : "이메일을 입력해주세요."}, status = status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(user, data=data, partial = True)
        try:
            serializer.is_valid(raise_exception = True)
            serializer.update(user, serializer.validated_data)
        except:
            return Response({"success" : False, "detail" : "이미 사용중인 이메일입니다."}, status= status.HTTP_400_BAD_REQUEST)
        return Response({"success" : True}, status = status.HTTP_200_OK)

    #주석처리 했는데 url이 인식되지 않음
    def list(self, request, pk=None):
         email = request.query_params.get('email')
         return Response({"detail" : email}, status = status.HTTP_200_OK)

class UserUpdateNicknameView(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserCreateSerializer
    def put(self, request, pk = None):
        user = request.user
        data = request.data.copy()
        if data.get('nickname') == None:
            return Response({"error" : "닉네임을 입력해주세요."}, status = status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(user, data=data, partial = True)
        try:
            serializer.is_valid(raise_exception = True)
            serializer.update(user, serializer.validated_data)
        except:
            return Response({"success" : False, "detail" : "이미 사용중인 닉네임입니다."}, status= status.HTTP_400_BAD_REQUEST)
        return Response({"success" : True}, status = status.HTTP_200_OK)

    def list(self, request, pk=None):
        nickname = request.data.get('nickname')
        return Response({"detail" : nickname}, status = status.HTTP_200_OK)

class UserUpdatePasswordView(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserCreateSerializer
    def put(self, request, pk = None):
        user = request.user
        data = request.data.copy()
        if data.get('password') == None:
            return Response({"error" : "비밀번호를 입력해주세요."}, status = status.HTTP_404_NOT_FOUND)
        try:
            validate_password(data.get('password'), user=request.user)
            user.set_password(data.get('password'))
            user.save()
        except:
            return Response({"success" : False, "detail" : "비밀번호가 잘못되었습니다."}, status= status.HTTP_400_BAD_REQUEST)
        return Response({"success" : True}, status = status.HTTP_200_OK)

    def list(self, request, pk=None):
        return Response({"detail" : "password"}, status = status.HTTP_200_OK)

class UserUpdateProfileImageView(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = UserCreateSerializer
    def put(self, request, pk = None):
        user = request.user
        data = request.data.copy()
        if data.get('profile_image') == None:
            return Response({"error" : "프로필 이미지를 첨부하세요."}, status = status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(user, data=data, partial = True)
        try:
            serializer.is_valid(raise_exception = True)
            serializer.update(user, serializer.validated_data)
        except:
            return Response({"success" : False, "detail" : "이미지 업로드 과정에서 오류가 발생했습니다."}, status= status.HTTP_400_BAD_REQUEST)
        return Response({"success" : True}, status = status.HTTP_200_OK)

    def list(self, request, pk=None):
        return Response({"detail" : "profile_image"}, status = status.HTTP_200_OK)

class UserFCMTokenView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        user = request.user
        data = request.data.copy()
        if (fcm_token:=data.get('fcm_token')) == None:
            return Response({"error" : "fcm_token missing"}, status = status.HTTP_400_BAD_REQUEST)
        
        User.objects.filter(fcm_token=fcm_token).update(fcm_token=None)
        user.fcm_token = fcm_token
        user.save()

        return Response({"success" : True}, status = status.HTTP_200_OK)

class UserNotificationViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )
    queryset = UserNotification.objects.all()

    #GET /notification/
    def list(self, request, pk=None):
        user = request.user
        user.notification_unread = 0
        user.save()
        
        queryset = self.queryset.filter(user=request.user).order_by('-id')
        return self.paginate(request, queryset)

    #GET /notification/{pk}/
    def retrieve(self, request, pk):
        if not (notification := UserNotification.objects.get(id=pk)):
            return Response(status=status.HTTP_404_NOT_FOUND, data={ "detail":"wrong_notification_id"})
        notification.unread = False
        notification.save()
        return Response(status=status.HTTP_200_OK, data={'success': True})

    #GET /notification/unread/
    @action(methods=['get'], detail=False)
    def unread(self, request):
        return Response(status=status.HTTP_200_OK, data={'unread_count': request.user.notification_unread})

    def paginate(self, request, queryset):
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = UserNotificationSerializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data) 
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="pagination fault")
