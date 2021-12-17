import random

from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import EmailCode
from django.core.mail import EmailMessage, BadHeaderError
from smtplib import SMTPException

# Create your views here.
class SetCodeToThisEmail(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, *args, **kwargs):
        #이메일 필드의 존재 확인
        if 'email' not in request.data:
            return Response({'email': 'email field is required'}, status=status.HTTP_404_NOT_FOUND)
        #이메일 앞뒤의 공백 제거
        request.data['email'] = request.data['email'].strip()
        #이메일에 랜덤한 수 할당
        if EmailCode.objects.filter(email=request.data['email']).exists():
            emailCode = EmailCode.objects.get(email=request.data['email'])
            emailCode.code = random.randint(1000, 9999)
        else:
            emailCode = EmailCode(email=request.data['email'], code=random.randint(1000, 9999))
        #메일 전송 및 에러 처리
        mail = EmailMessage("4자리 코드가 발급되었습니다", str(emailCode.code), to=[request.data['email']])
        try:
            mail.send(fail_silently=False)
        except BadHeaderError:  # If mail's Subject is not properly formatted.
            return Response({'email': 'Invalid header found.'}, status=status.HTTP_404_NOT_FOUND)
        except SMTPException as e:  # It will catch other errors related to SMTP.
            return Response({'email': 'There was an error sending an email.'}, status=status.HTTP_404_NOT_FOUND)
        except:  # It will catch All other possible errors.
            return Response({'email': 'Mail Sending Failed!'}, status=status.HTTP_404_NOT_FOUND)
        #성공적으로 메일이 전송된다면 최종적으로 emailCode를 저장한다.
        emailCode.save()
        return Response(status=status.HTTP_201_CREATED)

class CompareCode(APIView):
    def get(self, request, *args, **kwargs):
        if EmailCode.objects.filter(email=request.data['email'], code=request.data['code']).exists():
            return Response({'Result': 'Correct Code'}, status=status.HTTP_200_OK)
        else:
            return Response({'Result': 'Incorrect Code'}, status=status.HTTP_404_NOT_FOUND)

class EmailCodeViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /userCode/'}, status=status.HTTP_200_OK)