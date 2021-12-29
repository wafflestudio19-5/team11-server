from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

app_name = 'comment'

router = SimpleRouter()

#router.register('board/<int:board_id>/article', ArticleViewSet, basename='article') 
router.register(r'board/(?P<board_id>\d+)/article/(?P<article_id>\d+)/comment', CommentViewSet, basename='article')

#router.register(r'like/(?P<board_id>\d+)/article/(?P<article_id>\d+)/comment', CommentLikeViewSet, basename='article_')

urlpatterns = [
    path('', include(router.urls))
]