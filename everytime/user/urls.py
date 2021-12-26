from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserCheckEmailView, UserViewSet, UserLoginView, UserSignUpView, GetKakaoAccessCode, KakaoUserLoginView, KakaoUserSignUpView, UserCheckKakaoIdView

from user import views
router = SimpleRouter()
router.register('user', UserViewSet, basename='user')  # /api/v1/user/

urlpatterns = [
    path('register/', UserSignUpView.as_view(), name='signup'),  # /api/v1/signup/
    path('login/', UserLoginView.as_view(), name='login'),  # /api/v1/login/

    path('', include(router.urls), name='auth-user'),

    path('register/check_email/', UserCheckEmailView.as_view(), name = 'check_email'),
    path('register/check_kakao_id/', UserCheckKakaoIdView.as_view(), name='check_kakao_id'),

    path('register/oauth/', GetKakaoAccessCode.as_view(), name= 'access_code'),

    path('register/kakao/', KakaoUserSignUpView.as_view(), name='kakaosignup'),
    path('login/kakao/', KakaoUserLoginView.as_view(), name='kakaologin'),


]
