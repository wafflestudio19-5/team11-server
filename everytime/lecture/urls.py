from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *


app_name = 'lecture'

router = SimpleRouter()
router.register('lecture', LectureViewSet, basename='lecture')  # /api/v1/seminar/
router.register('subject_professor', SubjectProfessorViewSet, basename='subject_professor')
#router.register('board_favorite', UserBoardViewSet, basename='board_user')


urlpatterns = [
    path('', include(router.urls))
]
