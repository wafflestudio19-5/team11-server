from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

from user import views

app_name = 'article'

router = SimpleRouter()
router.register('board/article', ArticleViewSet, basename='article') 

urlpatterns = [
    path('', include(router.urls))
]