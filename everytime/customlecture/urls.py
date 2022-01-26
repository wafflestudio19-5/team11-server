from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

app_name = 'custom_lecture'

router = SimpleRouter()

#router.register('board/<int:board_id>/article', ArticleViewSet, basename='article') 

router.register(r'schedule/(?P<schedule_id>[-\w]+)/custom_lecture', CustomLectureViewSet, basename='article')


urlpatterns = [
    path('', include(router.urls))
]