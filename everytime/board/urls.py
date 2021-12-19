from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BoardViewSet, BoardList, AddBoard, CustomizedBoardList

from user import views
router = SimpleRouter()
router.register('board', BoardViewSet, basename='board')  # /api/v1/user/

urlpatterns = [
    path('register/board/', AddBoard.as_view(), name="AddBoard"),
    path('boardlist/', BoardList.as_view(), name="BoardList"),
    path('custom_boardList/', CustomizedBoardList.as_view(), name="BoardList"),
    path('', include(router.urls))
]
