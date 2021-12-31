from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

app_name = 'article'

router = SimpleRouter()

#router.register('board/<int:board_id>/article', ArticleViewSet, basename='article') 
router.register(r'board/(?P<board_id>\d+)/article', ArticleViewSet, basename='article')
router.register(r'like/article/(?P<article_id>\d+)', UserArticleLikeView, basename='article_like')
router.register(r'scrap/article/(?P<article_id>\d+)', UserArticleScrapView, basename='article_scrap')

urlpatterns = [
    path('', include(router.urls))
]