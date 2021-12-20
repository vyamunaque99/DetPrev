from django.db import models
from django.db.models.base import Model
from django.contrib.auth.models import User

# Create your models here.
class Dataset(models.Model):
    name=models.CharField(max_length=30,unique=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

