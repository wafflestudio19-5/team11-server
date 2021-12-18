from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UserCheckEmailView, UserCheckIDView, UserCheckUsernameView, UserViewSet, UserLoginView, UserSignUpView

from user import views
router = SimpleRouter()
router.register('user', UserViewSet, basename='user')  # /api/v1/user/

urlpatterns = [
    path('register/', UserSignUpView.as_view(), name='signup'),  # /api/v1/signup/
    path('login/', UserLoginView.as_view(), name='login'),  # /api/v1/login/
    path('', include(router.urls), name='auth-user'),
    path('register/check_id/', UserCheckIDView.as_view(), name = 'check_id'),
    path('register/check_email/', UserCheckEmailView.as_view(), name = 'check_email'),
    path('register/check_nickname/', UserCheckUsernameView.as_view(), name = 'check_nickname')
]
