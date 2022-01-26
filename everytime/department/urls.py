from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import CollegeViewSet, DepartmentViewSet


urlpatterns = [
    path('department/', DepartmentViewSet.as_view(), name='department'),
    path('college/', CollegeViewSet.as_view(), name='college')
]
