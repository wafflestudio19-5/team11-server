from rest_framework import serializers
from university.models import University
from allauth.socialaccount.models import SocialAccount
from requests import get
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.db import IntegrityError
from rest_framework_jwt.settings import api_settings

# 토큰 사용을 위한 기본 세팅
User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# [ user -> jwt_token ] function
def jwt_token_of(user):
    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)
    return jwt_token

class KakaoUserCreateSerializer(serializers.Serializer):

    access_token = serializers.CharField(required = True)
    name = serializers.CharField(required = True)
    email = serializers.EmailField(required=True)
    university = serializers.CharField(required = True)
    admission_year = serializers.IntegerField(required = True)
    nickname = serializers.CharField(required=True)

    def validate(self, data):
        university_name = data.get('university')
        try:
            university = University.objects.get(name = university_name)
        except :
            raise serializers.ValidationError("등록되지 않은 학교명입니다.")
        return data

    def create(self, validated_data):
        access_token = validated_data.pop('access_token')
        user_info_response = get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer ${access_token}'})

        if 'code' in user_info_response.json() and user_info_response.json().get('code') == -401:
            #raise serializers.ValidationError("유효하지 않은 access_token입니다")
            raise serializers.ValidationError

        kakao_id = user_info_response.json().get('id')

        if SocialAccount.objects.filter(uid=kakao_id, provider="kakao"):
            #raise serializers.ValidationError("카카오 계정이 이미 존재합니다")
            raise IntegrityError
            #return None, "이미 존재하는 카카오 계정"


        admission_year = validated_data.pop('admission_year')
        email = validated_data.pop('email')
        nickname = validated_data.pop('nickname')
        university_name = validated_data.pop('university')
        university = University.objects.get(name=university_name)
        name = validated_data.pop('name')

        user = User.objects.create(nickname=nickname, email=email, university=university, admission_year=admission_year, name=name)
        #allauth를 마스터하지 못한 탓에 좀 과격한 방식으로 SocialAccount 모델 생성
        SocialAccount.objects.create(uid=kakao_id, user=user, provider="kakao")
        return user, jwt_token_of(user)


class KakaoUserLoginSerializer(serializers.Serializer):

    # https://medium.com/chanjongs-programming-diary/django-rest-framework로-소셜-로그인-api-구현해보기-google-kakao-github-2-cf1b4059b5d5

    access_token = serializers.CharField(required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        access_token = data.get('access_token')

        #uid
        user_info_response = get('https://kapi.kakao.com/v2/user/me',
                                 headers={"Authorization": f'Bearer ${access_token}'})
        kakao_id = user_info_response.json().get('id')

        if kakao_id is None:
            raise serializers.ValidationError

        if not SocialAccount.objects.filter(uid=kakao_id, provider="kakao"):
            raise FileNotFoundError

        socialAccount = SocialAccount.objects.get(uid=kakao_id, provider="kakao")
        user = socialAccount.user

        update_last_login(None, user)
        return {
            'email': user.email,
            'token': jwt_token_of(user)
        }
