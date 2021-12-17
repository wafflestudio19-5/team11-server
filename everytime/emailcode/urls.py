from django.urls import path, include
from rest_framework.routers import SimpleRouter
from emailcode.views import SetCodeToThisEmail, CompareCode, EmailCodeViewSet

from user import views
router = SimpleRouter()
router.register('userCode', EmailCodeViewSet, basename='userCode')  # /api/v1/user/

urlpatterns = [
    path('CompareCode/', CompareCode.as_view(), name="CompareCode"),
    path('SetCodeToThisEmail/', SetCodeToThisEmail.as_view(), name='SetCodeToThisEmail'),
    path('', include(router.urls))
]
