from django.db import models
from user.models import User
from common.models import BaseModel
from lecture.models import Lecture

# Create your models here.
class Schedule(BaseModel):

    @classmethod
    def get_default_schedule(cls, user):
        if not Schedule.objects.filter(user=user):
            return None
        return Schedule.objects.filter(user=user).order_by('last_visit').last()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    season = models.IntegerField()
    last_visit = models.DateTimeField(auto_now=True)



