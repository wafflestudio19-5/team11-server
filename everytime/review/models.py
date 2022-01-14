from django.db import models
from user.models import User
from common.models import BaseModel
from lecture.models import Lecture

# Create your models here.
class Review(BaseModel):
    HomeworkCode = {0: "없음", 1: "보통", 2: "많음",
                    "없음": 0, "보통": 1, "많음": 2}
    TeamActivityCode = {0: "없음", 1: "보통", 2: "많음",
                        "없음": 0, "보통": 1, "많음": 2}
    GradingCode = {0: "너그러움", 1: "보통", 2: "깐깐함",
                   "너그러움": 0, "보통": 1, "깐깐함": 2}
    AttendanceCode = {0: "혼용", 1: "직접호명", 2: "지정좌석", 3: "전자출결", 4: "반영안함",
                      '혼용': 0, '직접호명': 1, '지정좌석': 2, '전자출결': 3, '반영안함': 4}
    TestCountCode = {0: "없음", 1: "한번", 2: "두번", 3: "세번", 4: "네번이상",
                     "없음": 0, "한번": 1, "두번": 2, '세번': 3, '네번이상': 4}

    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField()
    homework = models.IntegerField()
    team_activity = models.IntegerField()
    grading = models.IntegerField()
    attendance = models.IntegerField()
    test_count = models.IntegerField()
    comment = models.CharField(max_length=1000)



