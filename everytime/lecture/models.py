from django.db import models
from department.models import College, Department
from user.models import User
from common.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
class SubjectProfessor(BaseModel):
    subject_name = models.CharField(max_length=100, null = False)
    professor = models.CharField(max_length=100, blank=True)

class Lecture(BaseModel):

    SeasonCode = {1: "1학기", 2: "2학기", 3: "여름학기", 4: "겨울학기",
                  "1학기": 1, "2학기": 2, "여름학기": 3, "겨울학기": 4}

    LevelCode = {"학사": 1, "학석사통합": 2, "석사": 3, "석박사통합": 4, "박사": 5,
                 1: "학사", 2: "학석사통합", 3: "석사", 4: "석박사통합", 5: "박사"}

    CategoryCode = {'교양': 1, '전선': 2, '전필': 3, '교직':4, '대학원':5, '논문':6, '일선':7, '공통':8,
                    1: '교양', 2: '전선', 3: '전필', 4: '교직', 5: '대학원', 6: '논문', 7: '일선', 8: '공통'}

    subject_professor = models.ForeignKey(SubjectProfessor, on_delete=models.CASCADE, related_name='prof_lecture')
    subject_code = models.CharField(max_length=100, null=False)
    ######
    year = models.IntegerField()
    season = models.IntegerField()
    ######
    method = models.CharField(max_length=50, blank=True, default='')
    quota = models.IntegerField(default=0)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department_lecture', null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='college_lecture', null=True)
    grade = models.IntegerField()
    level = models.IntegerField()
    credit = models.IntegerField()
    category = models.IntegerField() # 분류
    number = models.IntegerField() # 강좌번호
    detail = models.CharField(null=True, max_length=1000)
    language = models.CharField(max_length=100)
    ####
    time = models.CharField(max_length=300, null=True)
    location = models.CharField(max_length=300, null=True)









