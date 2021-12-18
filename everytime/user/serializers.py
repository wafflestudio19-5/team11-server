from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from university.models import University

# 토큰 사용을 위한 기본 세팅
User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# [ user -> jwt_token ] function
def jwt_token_of(user):
    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)
    return jwt_token


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
        except University.DoesNotExist:
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