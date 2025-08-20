from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    result = models.IntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)
    last_streak_check = models.DateField(null=True, blank=True)