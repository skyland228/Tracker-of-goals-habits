from django.db import models
from django.contrib.auth.models import  AbstractUser
import uuid
from django.utils import timezone 
from datetime import timedelta
from django.conf import settings

class TelegramLinkToken(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  token = models.CharField(max_length=64,unique=True)
  used = models.BooleanField(default=False)
  expires_at = models.DateTimeField()

  @staticmethod
  def create_token(user):
    return TelegramLinkToken.objects.create(user = user, token = uuid.uuid4().hex,
                                            expires_at = timezone.now() + timedelta(minutes=5))


class User(AbstractUser):
  image = models.ImageField(upload_to='users/%Y/%m/%d/', blank = True, verbose_name='Фото')
  bio = models.TextField(blank = True, verbose_name='Биография')
  telegram_id = models.IntegerField(blank=True, null = True)



