from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

from user import views

app_name = 'board'

router = SimpleRouter()
router.register('board', BoardViewSet, basename='board')  # /api/v1/seminar/
router.register('board_favorite', UserBoardViewSet, basename='board_user')

urlpatterns = [
    path('', include(router.urls))
]
