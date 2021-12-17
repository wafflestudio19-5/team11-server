from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import AddDepartment, DepartmentViewSet

from user import views
router = SimpleRouter()
router.register('department', DepartmentViewSet, basename='department')  # /api/v1/user/

urlpatterns = [
    path('AddDepartment/', AddDepartment.as_view(), name="AddDepartment"),
    path('', include(router.urls))
]
