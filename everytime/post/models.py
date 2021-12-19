from django.db import models
from board.models import Board
# Create your models here.
from common.models import BaseModel
from django.utils import timezone
from user.models import User

class Post(BaseModel):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='board_posts')
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(default=timezone.now)
    is_anonymous = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

class PostImage(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_postImages")
    image = models.ImageField(upload_to="images/post/", null=True, blank=True)
    is_active = models.BooleanField(default=True)


class UserPost(BaseModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_UserPosts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_UserPosts")
    is_owner = models.BooleanField(default=False)
    has_liked = models.BooleanField(default=False)
    has_scrapped = models.BooleanField(default=False)



