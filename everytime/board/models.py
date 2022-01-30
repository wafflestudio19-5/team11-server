from django.db import models
from user.models import User
from university.models import University

# Create your models here.
from common.models import BaseModel

class Board(BaseModel):

    # https://stackoverflow.com/questions/18676156/how-to-properly-use-the-choices-field-option-in-django
    class BoardType(models.IntegerChoices):
        DEF = 0, 'default'
        CAR = 1, 'career'
        PRO = 2, 'promotion'
        ORG = 3, 'organization'
        DEP = 4, 'department'
        GEN = 5, 'general'

    name = models.CharField(max_length=100, null = False)
    university = models.ForeignKey(University, on_delete=models.PROTECT, related_name='boards')
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='manager', null=True)
    type = models.PositiveSmallIntegerField(choices=BoardType.choices, default=BoardType.GEN)
    description = models.CharField(max_length=100, default="")
    allow_anonymous = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.name
    
class UserBoard(BaseModel):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='user_board', null=True)
    board = models.ForeignKey(Board, on_delete=models.SET_NULL, related_name='user_board', null=True)
    favorite = models.BooleanField(default=True)
