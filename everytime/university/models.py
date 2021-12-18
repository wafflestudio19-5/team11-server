from django.db import models

# Create your models here.
from common.models import BaseModel
class University(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    email_domain = models.CharField(max_length=100) #서울대의 경우 snu.ac.kr을 저장
