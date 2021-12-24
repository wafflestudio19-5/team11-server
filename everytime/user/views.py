from requests import post, get
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import IntegrityError
from user.serializers import UserCreateSerializer, UserLoginSerializer,KakaoUserLoginSerializer, KakaoUserCreateSerializer
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

class KakaoUserSignUpView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = KakaoUserCreateSerializer(data=request.data)
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

class KakaoUserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = KakaoUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        return Response({'success': True, 'token': token}, status=status.HTTP_200_OK)

class GetKakaoAccessCode(APIView):
    # https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=52ea0391142c816eccc27171813198f6&redirect_uri=http://127.0.0.1:8000/api/v1/register/oauth
    def get(self, request):
        auth_code = request.GET.get('code')
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': '52ea0391142c816eccc27171813198f6',
            'redirection_uri': 'http://localhost:8000/users/signin/kakao/callback',
            'code': auth_code
        }
        token_response = post(kakao_token_api, data=data)
        access_token = token_response.json().get('access_token')
        return Response(access_token)
        ##user_info_response = get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})

        #print(user_info_response.json())
        #return Response(user_info_response.json().get('id'))

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

class UserCheckKakaoIdView(APIView):
    permissions_classes = (permissions.AllowAny, )
    def get(self, request, *args, **kwargs):
        queryset = User.objects.all()
        data = request.query_params

        access_token = data.get('access_token')

        if not access_token:
            return Response({'access token을 입력해주세요.'}, status = status.HTTP_400_BAD_REQUEST)

        user_info_response = get('https://kapi.kakao.com/v2/user/me',
                                 headers={"Authorization": f'Bearer ${access_token}'})

        print(user_info_response.json())

        if "id" not in user_info_response.json():
            return Response({'유효하지 않은 access token입니다'}, status = status.HTTP_401_UNAUTHORIZED)

        kakao_id = user_info_response.json().get('id')


        for user in queryset:
            if user.kakao_id == kakao_id:
                return Response({"check" : "False" , "detail" : '이미 사용중인 카카오 계정입니다.'}, status = status.HTTP_302_FOUND)
        return Response({"check" : "True", "detail" : "가입 가능한 계정입니다."}, status = status.HTTP_200_OK)

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

class UserViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /user/'}, status=status.HTTP_200_OK)