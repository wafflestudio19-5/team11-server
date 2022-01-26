import re
from django.db import models
from university.models import University
# Create your models here.
from common.models import BaseModel

class College(BaseModel):
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='colleges')

class Department(BaseModel):
    name = models.CharField(max_length=100)
    college = models.ForeignKey(College, on_delete=models.CASCADE, related_name='departments', default=None)