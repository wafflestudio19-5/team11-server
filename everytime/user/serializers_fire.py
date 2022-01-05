from rest_framework import serializers
from university.models import University
from allauth.socialaccount.models import SocialAccount
from requests import get
from .models import User
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.db import IntegrityError
from rest_framework_jwt.settings import api_settings

import firebase_admin
from firebase_admin import credentials, auth


# 토큰 사용을 위한 기본 세팅
User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# [ user -> jwt_token ] function
def jwt_token_of(user):
    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)
    return jwt_token

class FireBaseUserCreateSerializer(serializers.Serializer):

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

        try:
            decoded_token = auth.verify_id_token(access_token)
            uid = decoded_token['uid']
        except ...:
            raise serializers.ValidationError

        if SocialAccount.objects.filter(uid=uid, provider="fire"):
            raise IntegrityError

        admission_year = validated_data.pop('admission_year')
        email = validated_data.pop('email')
        nickname = validated_data.pop('nickname')
        university_name = validated_data.pop('university')
        university = University.objects.get(name=university_name)
        name = validated_data.pop('name')

        user = User.objects.create(nickname=nickname, email=email, university=university, admission_year=admission_year, name=name)
        #allauth를 마스터하지 못한 탓에 좀 과격한 방식으로 SocialAccount 모델 생성
        SocialAccount.objects.create(uid=uid, user=user, provider="fire")
        return user, jwt_token_of(user)


class FireBaseUserLoginSerializer(serializers.Serializer):

    # https://medium.com/chanjongs-programming-diary/django-rest-framework로-소셜-로그인-api-구현해보기-google-kakao-github-2-cf1b4059b5d5

    access_token = serializers.CharField(required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        access_token = data.get('access_token')

        #uid
        try:
            decoded_token = auth.verify_id_token(access_token)
            uid = decoded_token['uid']
        except Exception:
            raise serializers.ValidationError("카카오 계정이 존재하지 않습니다")

        if not SocialAccount.objects.filter(uid=uid, provider="fire"):
            raise serializers.ValidationError("카카오 계정이 존재하지 않습니다")

        socialAccount = SocialAccount.objects.get(uid=uid, provider="fire")
        user = socialAccount.user

        update_last_login(None, user)
        return {
            'email': user.email,
            'token': jwt_token_of(user)
        }
