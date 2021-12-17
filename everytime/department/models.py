from django.db import models
from university.models import University
# Create your models here.
from common.models import BaseModel

class Department(BaseModel):
    name = models.CharField(max_length=100)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='university_departments')

