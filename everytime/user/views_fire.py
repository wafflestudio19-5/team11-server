from rest_framework import permissions, status
from rest_framework.views import APIView
from .serializers_fire import *
from django.db import IntegrityError
from rest_framework.response import Response
from requests import post


class FireBaseUserSignUpView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = FireBaseUserCreateSerializer(data=request.data)
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


class FireBaseUserLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = FireBaseUserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']

        return Response({'success': True, 'token': token}, status=status.HTTP_200_OK)
