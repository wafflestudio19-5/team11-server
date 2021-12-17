from django.db import models
from common.models import BaseModel
# Create your models here.
class EmailCode(BaseModel):
    email = models.CharField(max_length=100, blank=False)
    code = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
