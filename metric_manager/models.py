from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=20)
    password =  models.CharField(max_length=20)
    age = models.FloatField(max_length=20)
    weight = models.FloatField(max_length=20)
    height = models.FloatField(max_length=20)
    birthdate = models.DateField()
