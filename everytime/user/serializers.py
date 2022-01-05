from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.db.models import fields
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from university.models import University
from user.models import User


# 토큰 사용을 위한 기본 세팅
User = get_user_model()
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# [ user -> jwt_token ] function
def jwt_token_of(user):
    payload = JWT_PAYLOAD_HANDLER(user)
    jwt_token = JWT_ENCODE_HANDLER(payload)
    return jwt_token


class UserCreateSerializer(serializers.ModelSerializer):

    university = serializers.CharField(required = True)
    user_id = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'user_id',
            'name',
            'email',
            'nickname',
            'password',
            'university',
            'admission_year',
            'is_active',
            'profile_image'
        )

    def validate(self, data):
        # create 시에만 작동. update할때는 작동하지 않음.
        if not self.instance:
            university_name = data.get('university')
            try:
                university = University.objects.get(name = university_name)
            except:
                raise serializers.ValidationError("등록되지 않은 학교명입니다.")

        return data
    
    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email')
    #     instance.nickname = validated_data.get('nickname')
    #     instance.password = validated_data.get('password')
    #     instance.is_active = validated_data.get('is_active')
    #     instance.save()
    #     return instance

    def create(self, validated_data):
        admission_year = validated_data.pop('admission_year')
        email = validated_data.pop('email')
        nickname = validated_data.pop('nickname')
        password = validated_data.pop('password')
        user_id = validated_data.pop('user_id')
        university_name = validated_data.pop('university')
        university = University.objects.get(name = university_name)
        name = validated_data.pop('name')
        user = User.objects.create_user(user_id = user_id, nickname = nickname, email = email, password = password, university = university, admission_year = admission_year, name = name)
        return user, jwt_token_of(user)

class UserLoginSerializer(serializers.Serializer):
    
    user_id = serializers.CharField(max_length=64, required=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        user_id = data.get('user_id', None)
        password = data.get('password', None)

        # USERNAME_FIELD가 email이기 때문에 해당 user_id의 email을 받은 후 authenticate
        try:
            user = User.objects.get(user_id=user_id)
        except:
            raise serializers.ValidationError("아이디가 존재하지 않습니다.") #존재하지 않는 아이디
        email = user.email

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("비밀번호가 잘못되었습니다.") #비밀번호 오류

        update_last_login(None, user)
        return {
            'user_id': user.user_id,
            'token': jwt_token_of(user)
        }


