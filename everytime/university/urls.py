from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import UniversityViewSet, UniversityList

from user import views
router = SimpleRouter()
router.register('university', UniversityViewSet, basename='university')  # /api/v1/user/

urlpatterns = [
    path('register/university/', UniversityList.as_view(), name="university"),
    path('', include(router.urls)),
]
