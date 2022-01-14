from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *


app_name = 'information'

router = SimpleRouter()
router.register(r'subject_professor/(?P<subject_professor_id>\d+)/information', InformationViewSet, basename='article')
#router.register('board_favorite', UserBoardViewSet, basename='board_user')


urlpatterns = [
    path('', include(router.urls))
]
