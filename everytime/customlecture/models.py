from django.db import models
from user.models import User
from common.models import BaseModel
from lecture.models import Lecture
from schedule.models import Schedule

# Create your models here.
class CustomLecture(BaseModel):
    @classmethod
    def string_to_time_set(cls, time):
        if not time:
            return set()
        set_time = set()
        times = time.split('/')
        if times == ['']:
            return set_time
        for time in times:
            weekdays = time.split('(')[0]
            start_code, end_code = (time.split('(')[1][:-1]).split('~')
            start, end = start_code.split(':'), end_code.split(':')
            start = (int(start[0]), int(start[1]))
            end = (int(end[0]), int(end[1]))

            set_time.add((weekdays, start, end))
        return set_time

    def get_time(self):
        return self.string_to_time_set(self.time)

    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, null=True, on_delete=models.SET_NULL)
    nickname = models.CharField(max_length=100, null=True)
    professor = models.CharField(max_length=100, null=True)

    # 시간이 비어있을 수 있음
    time = models.CharField(max_length=300, null=True)
    location = models.CharField(max_length=300, null=True)
    memo = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)




