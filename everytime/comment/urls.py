from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

app_name = 'comment'

router = SimpleRouter()

#router.register('board/<int:board_id>/article', ArticleViewSet, basename='article') 
router.register(r'board/(?P<board_id>\d+)/article/(?P<article_id>\d+)/comment', CommentViewSet, basename='comment')
router.register(r'like/comment/(?P<comment_id>\d+)', UserCommentLikeView, basename='comment_like')

urlpatterns = [
    path('', include(router.urls))
]