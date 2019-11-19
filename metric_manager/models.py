from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class FitbitUser(AbstractUser):
    weight = models.FloatField(max_length=20)
    height = models.FloatField(max_length=20)
    birthdate = models.DateField()

class Metrics(models.Model):
    user_fk = models.ForeignKey(
		FitbitUser,
		on_delete=models.CASCADE,
        null=True
	)
    timestamp = models.DateTimeField(default=now)
    amount = models.FloatField(max_length=20)
    type = models.CharField(max_length=15)
