from rest_framework import serializers, status, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class UserSignUpView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        return Response({'detail': 'POST /signup/'}, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        return Response({'detail': 'GET /signup/'}, status=status.HTTP_200_OK)

class UserLoginView(APIView):
    permission_classes = (permissions.AllowAny, )
    
    def post(self, request):
        return Response({'detail': 'POST /login/'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated, )

    def retrieve(self, request, pk=None):
        return Response({'detail': 'GET /user/'}, status=status.HTTP_200_OK)
