from rest_framework import permissions, status
from rest_framework.views import APIView
from .serializers_kakao import *
from django.db import IntegrityError
from rest_framework.response import Response
from requests import post

class KakaoUserSignUpView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        serializer = KakaoUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user, jwt_token = serializer.save()
        except IntegrityError:
            return Response(status=status.HTTP_409_CONFLICT, data='중복되는 계정입니다. 중복확인 제대로 했는지 확인해주세요.')
        except serializers.ValidationError:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="유효하지 않은 access token입니다.")

        if user is None:
            return Response(data="")

        return Response({'email': user.email, 'token': jwt_token}, status=status.HTTP_201_CREATED)
class KakaoUserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = KakaoUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        return Response({'success': True, 'token': token}, status=status.HTTP_200_OK)

class GetKakaoAccessCode(APIView):
    permission_classes = (permissions.AllowAny,)
    # 테스트용 함수. 아래 링크를 클릭하면 /register/oauth/로 리다이렉트 되고 access_token을 확인할 수 있음
    # https://kauth.kakao.com/oauth/authorize?response_type=code&client_id=52ea0391142c816eccc27171813198f6&redirect_uri=http://127.0.0.1:8000/api/v1/register/oauth
    def get(self, request):
        #인가 코드 받기
        auth_code = request.GET.get('code')
        #access_token 받기
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': '52ea0391142c816eccc27171813198f6',
            'redirection_uri': 'http://localhost:8000/users/signin/kakao/callback',
            'code': auth_code
        }
        token_response = post(kakao_token_api, data=data)
        access_token = token_response.json().get('access_token')
        #유저 정보 받기
        user_info_response = get('https://kapi.kakao.com/v2/user/me',
                                 headers={"Authorization": f'Bearer ${access_token}'})

        #print(user_info_response.json())
        
        return Response({"access_token": access_token, "info": user_info_response.json()})
