from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *


app_name = 'review'

router = SimpleRouter()
router.register(r'subject_professor/(?P<subject_professor_id>\d+)/review', ReviewViewSet, basename='article')
router.register(r'subject_professor/all/review', ReviewAllViewSet, basename='reviewall')
#router.register('board_favorite', UserBoardViewSet, basename='board_user')


urlpatterns = [
    path('', include(router.urls))
]
