from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *


app_name = 'schedule'

router = SimpleRouter()
router.register('schedule', ScheduleViewSet, basename='schedule')  # /api/v1/seminar/
#router.register('board_favorite', UserBoardViewSet, basename='board_user')


urlpatterns = [
    path('', include(router.urls))
]
