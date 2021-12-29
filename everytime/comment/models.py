from django.db import models
from article.models import Article
from user.models import User
from common.models import BaseModel

class Comment(BaseModel):
    
    pass
    #disable for partial deploy
    # article = models.ForeignKey(Article, on_delete=models.CASCADE) 
    # parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True)
    # text = models.CharField(max_length=300, null = False)
    # created_at = models.DateTimeField(auto_now_add=True)
    # commenter = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comments', null = True)
    # like_count = models.PositiveIntegerField(default=0)
    # is_writer = models.BooleanField(default=False, null = False)
    # is_anonymous = models.BooleanField(default=True, null = False)
    # is_active = models.BooleanField(default=True, null = False)

    # Serializer field only
    #is_mine True,