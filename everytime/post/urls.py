from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import WritePost, PostViewSet, SearchPost
from django.conf import settings
from django.conf.urls.static import static

from user import views
router = SimpleRouter()
router.register('post', PostViewSet, basename='post')  # /api/v1/user/

urlpatterns = [
    path('api/v1/WritePost/', WritePost.as_view(), name="WritePost"),
    path('api/v1/SearchPost/', SearchPost.as_view(), name="SearchPost"),
    path('', include(router.urls))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
