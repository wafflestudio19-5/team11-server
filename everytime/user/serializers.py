from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from university.models import University
from .models import User
from requests import get

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

    access_token = serializers.CharField(required=True)
    name = serializers.CharField(required = True)
    email = serializers.EmailField(required=True)
    university = serializers.CharField(required = True)
    admission_year = serializers.IntegerField(required = True)

    def validate(self, data):
        university_name = data.get('university')
        try:
            university = University.objects.get(name = university_name)
        except :
            raise serializers.ValidationError("등록되지 않은 학교명입니다.")
        return data

    def create(self, validated_data):
        access_token = validated_data.pop('access_token')
        user_info_response = get('https://kapi.kakao.com/v2/user/me',headers={"Authorization": f'Bearer ${access_token}'})
        #print(user_info_response.json())
        kakao_id = user_info_response.json().get('id')

        admission_year = validated_data.pop('admission_year')
        email = validated_data.pop('email')
        nickname = user_info_response.json().get('properties').get('nickname')
        university_name = validated_data.pop('university')
        university = University.objects.get(name=university_name)
        name = validated_data.pop('name')

        user = User.objects.create(kakao_id=kakao_id, nickname=nickname, email=email, university=university, admission_year=admission_year, name=name)

        return user, jwt_token_of(user)

class KakaoUserLoginSerializer(serializers.Serializer):
    access_token = serializers.CharField(required=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        access_token = data.get('access_token')

        user_info_response = get('https://kapi.kakao.com/v2/user/me',
                                 headers={"Authorization": f'Bearer ${access_token}'})

        kakao_id = user_info_response.json().get('id')

        user = User.objects.get(kakao_id=kakao_id)

        if user is None:
            raise serializers.ValidationError("카카오 계정이 존재하지 않습니다.")

        update_last_login(None, user)
        return {
            'user_id': user.user_id,
            'token': jwt_token_of(user)
        }

class UserCreateSerializer(serializers.Serializer):

    user_id = serializers.CharField(required = True)
    name = serializers.CharField(required = True)
    email = serializers.EmailField(required=True)
    nickname = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    university = serializers.CharField(required = True)
    admission_year = serializers.IntegerField(required = True)

    def validate(self, data):
        university_name = data.get('university')
        try:
            university = University.objects.get(name = university_name)
        except :
            raise serializers.ValidationError("등록되지 않은 학교명입니다.")
        return data

    def create(self, validated_data):
        admission_year = validated_data.pop('admission_year')
        email = validated_data.pop('email')
        nickname = validated_data.pop('nickname')
        password = validated_data.pop('password')
        user_id = validated_data.pop('user_id')
        university_name = validated_data.pop('university')
        university = University.objects.get(name = university_name)
        user = User.objects.create_user(user_id = user_id, nickname = nickname, email = email, password = password, university = university, admission_year = admission_year)
        return user, jwt_token_of(user)

class UserLoginSerializer(serializers.Serializer):
    
    user_id = serializers.CharField(max_length=64, required=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user_id = data.get('user_id', None)
        password = data.get('password', None)
        user = authenticate(user_id=user_id, password=password)

        if user is None:
            raise serializers.ValidationError("이메일 또는 비밀번호가 잘못되었습니다.")

        update_last_login(None, user)
        return {
            'user_id': user.user_id,
            'token': jwt_token_of(user)
        }

