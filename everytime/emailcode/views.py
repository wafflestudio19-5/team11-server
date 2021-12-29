import random

from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import EmailCode
from django.core.mail import EmailMessage, BadHeaderError
from smtplib import SMTPException

# Create your views here.
class Code(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        #이메일 필드의 존재 확인

        email = request.query_params.get('email')

        if not email:
            return Response({'email': 'email field is required'}, status=status.HTTP_404_NOT_FOUND)

        #이메일 앞뒤의 공백 제거
        email = email.strip()
        #이메일에 랜덤한 수 할당
        if EmailCode.objects.filter(email=email).exists():
            emailCode = EmailCode.objects.get(email=email)
            emailCode.code = random.randint(1000, 9999)
        else:
            emailCode = EmailCode(email=email, code=random.randint(1000, 9999))
        #메일 전송 및 에러 처리
        mail = EmailMessage("4자리 코드가 발급되었습니다", str(emailCode.code), to=[email])
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

    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        code = request.query_params.get('code')

        error = {}
        if not email:
            error["email"] = "This field is required."
        if not code:
            error["code"] = "This field is required."

        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        email = email.strip()

        if EmailCode.objects.filter(email=email, code=code).exists():
            return Response({'Result': 'Correct Code'}, status=status.HTTP_200_OK)
        else:
            return Response({'Result': 'Incorrect Code'}, status=status.HTTP_404_NOT_FOUND)


class EmailCodeViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /userCode/'}, status=status.HTTP_200_OK)
