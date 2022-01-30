from django.db import models
from university.models import University
from board.models import Board
from user.models import User
from common.models import BaseModel

from user.utils import upload_image

class Article(BaseModel):
    title = models.CharField(max_length=100, null = False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='articles', null = True)
    writer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='articles', null = True)
    text = models.CharField(max_length=5000, null = False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=True)
    is_question = models.BooleanField(default=False)

    def __str__(self):
        return "[" + str(self.id) + "] : " + self.title + " / " + self.text[0:20] + " ..."

class UserArticle(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_article', null = True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='user_article', null = False)
    like = models.BooleanField(default = False, null = False)
    scrap = models.BooleanField(default = False, null = False)
    subscribe = models.BooleanField(default = False, null = False)
    nickname_code = models.PositiveSmallIntegerField(null = True)
    
    # nickname_code - 익명 표시
    # null : "익명"
    # 0 : 익명(글쓴이)
    # 1~ : 익명 1

class ImageArticle(BaseModel):
    image = models.ImageField(upload_to = upload_image, editable = False, null = False)
    description = models.CharField(max_length=5000, null = True)
    article = models.ForeignKey(Article, on_delete=models.SET_NULL, related_name='images', null = True)