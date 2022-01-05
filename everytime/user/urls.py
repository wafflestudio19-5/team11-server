from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *
from .views_kakao import *


router = SimpleRouter()
router.register('user', UserViewSet, basename='user')  # /api/v1/user/

router1 = SimpleRouter()

router1.register('my/email', UserUpdateEmailView, basename='my_email')
router1.register('my/nickname', UserUpdateNicknameView, basename='my_nickname')
router1.register('my/password', UserUpdatePasswordView, basename = 'my_password')
router1.register('my', UserViewSet, basename = 'my')
router1.register('my/withdrawal', UserDeleteViewset, basename = 'my_withdrawal')

urlpatterns = [
    path('register/', UserSignUpView.as_view(), name='signup'),  # /api/v1/signup/
    path('login/', UserLoginView.as_view(), name='login'),  # /api/v1/login/
    path('', include(router.urls), name='auth-user'),
    path('', include(router1.urls), name = 'update'),
    path('register/check_id/', UserCheckIDView.as_view(), name = 'check_id'),
    path('register/check_email/', UserCheckEmailView.as_view(), name = 'check_email'),
    path('register/check_nickname/', UserCheckUsernameView.as_view(), name = 'check_nickname'),

    path('register/kakao/', KakaoUserSignUpView.as_view(), name='kakaosignup'),
    path('login/kakao/', KakaoUserLoginView.as_view(), name='kakaologin'),
    path('register/oauth/', GetKakaoAccessCode.as_view(), name= 'access_code'),
]
