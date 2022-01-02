from django.urls import path, include
from rest_framework.routers import SimpleRouter
from emailcode.views import Code, EmailCodeViewSet

from user import views
router = SimpleRouter()
router.register('userCode', EmailCodeViewSet, basename='userCode')  # /api/v1/user/

urlpatterns = [
    path('email_code/', Code.as_view(), name='email_code'),
    path('', include(router.urls))
]
