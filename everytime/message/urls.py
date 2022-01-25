from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

app_name = 'message'

router = SimpleRouter()

router.register(r'message', MessageViewSet, basename='message')
router.register(r'message_room', MessageRoomViewSet, basename='message_room')
#router.register(r'message/count', UserCommentLikeView, basename='comment_like')


urlpatterns = [
    path('', include(router.urls))
]