from django.db import models
from user.models import User
from common.models import BaseModel
from lecture.models import Lecture
from schedule.models import Schedule

# Create your models here.
class CustomLecture(BaseModel):
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, null=True, on_delete=models.SET_NULL)
    nickname = models.CharField(max_length=100)
    professor = models.CharField(max_length=100, null=True)
    time = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True)
    memo = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)




