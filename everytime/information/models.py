from django.db import models
from user.models import User
from common.models import BaseModel
from lecture.models import Lecture, SubjectProfessor
# Create your models here.
class Information(BaseModel):

    TestMethodCode = {1: '객관식', 2: '주관식', 3: 'T/F형', 4: '약술형', 5: '논술형', 6:'구술', 7: '기타',
                      '객관식': 1, '주관식': 2, 'T/F형': 3, '약술형': 4, '논술형': 5, '구술': 6, '기타': 7}

    subject_professor = models.ForeignKey(SubjectProfessor, on_delete=models.CASCADE)
    year = models.IntegerField()
    season = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test_number = models.IntegerField() # 기타는 0번
    test_method = models.IntegerField()
    strategy = models.CharField(max_length=1000)
    problems = models.CharField(max_length=1000)



