from django.db import models
from django.contrib.auth.models import  AbstractUser

class User(AbstractUser):
  image = models.ImageField(upload_to='users/%Y/%m/%d/', blank = True, verbose_name='Фото')
  bio = models.TextField(blank = True, verbose_name='Биография')
  telegram_id = models.IntegerField(blank=True, null = True)



