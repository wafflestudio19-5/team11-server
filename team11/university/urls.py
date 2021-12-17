from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UniversityViewSet, UniversityList, AddUniversity

from user import views
router = SimpleRouter()
router.register('university', UniversityViewSet, basename='university')  # /api/v1/user/

urlpatterns = [
    path('UniversityList/', UniversityList.as_view(), name="UniversityList"),
    path("AddUniversity/", AddUniversity.as_view(), name="AddUniversity"),
    path('', include(router.urls))
]
