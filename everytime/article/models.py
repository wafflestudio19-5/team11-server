from django.db import models
from university.models import University
from board.models import Board
from user.models import User
from common.models import BaseModel

class Article(BaseModel):
    title = models.CharField(max_length=100, null = False)
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, related_name='articles', null = True)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='articles', null = True)
    text = models.CharField(max_length=5000, null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=True)
    is_question = models.BooleanField(default=False)