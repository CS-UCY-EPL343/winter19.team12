from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class FitbitUser(AbstractUser):
    weight = models.FloatField(max_length=20,null=True)
    height = models.FloatField(max_length=20,null=True)
    birthdate = models.DateField(null=True)
    telephone = models.CharField(max_length=15,null=True)
    gender = models.CharField(max_length=10,null=True)
    address = models.CharField(max_length=20,null=True)
    is_specialist = models.BooleanField(default=False)

class Monitor(models.Model):
    spec_fk = models.ForeignKey(
		FitbitUser,
        related_name='%(class)s_specialist',
		on_delete=models.CASCADE,
        null=True
	)
    user_fk = models.ForeignKey(
		FitbitUser,
        related_name='%(class)s_user',
		on_delete=models.CASCADE,
        null=True
	)

class PermissionRequest(models.Model):
    from_user = models.ForeignKey(
		FitbitUser,
        related_name='%(class)s_from',
		on_delete=models.CASCADE
	)
    to_user = models.ForeignKey(
		FitbitUser,
        related_name='%(class)s_to',
		on_delete=models.CASCADE
	)
    completed = models.BooleanField(default=False)

class MetricsDescription(models.Model):
    metric_name = models.CharField(max_length=20)


class Metrics(models.Model):
    user_fk = models.ForeignKey(
		FitbitUser,
        related_name='%(class)s_user',
		on_delete=models.CASCADE,
        null=True
	)

    timestamp = models.DateTimeField(default=now)
    amount = models.FloatField(max_length=20)
    type = models.ForeignKey(
		MetricsDescription,
		on_delete=models.CASCADE,
        null=True
	)

class Notes(models.Model):
    id_writer = models.ForeignKey(
		FitbitUser,
        related_name='%(class)s_writer',
		on_delete=models.CASCADE,
        null=True
	)
    id_reader = models.ForeignKey(
		FitbitUser,
        related_name='%(class)s_reader',
        on_delete=models.CASCADE,
        null=True
	)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
