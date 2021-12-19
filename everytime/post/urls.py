from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import WritePost, PostViewSet, SearchPostTitle, SearchPostKeyword, GetPost, DeletePostImage
from django.conf import settings
from django.conf.urls.static import static

from user import views
router = SimpleRouter()
router.register('post', PostViewSet, basename='post')  # /api/v1/user/

urlpatterns = [
    path('api/v1/WritePost/', WritePost.as_view(), name="WritePost"),
    path('api/v1/SearchPostTitle/', SearchPostTitle.as_view(), name="SearchPostTitle"),
    path('api/v1/SearchPostKeyword/', SearchPostKeyword.as_view(), name="SearchPostKeyword"),
    path('api/v1/GetPost/', GetPost.as_view(), name="GetPost"),
    path('api/v1/DeletePostImage/', DeletePostImage.as_view(), name="DeletePostImage"),
    path('', include(router.urls))
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
