from django.db import models
from django.contrib.auth import get_user_model

class Profile(models.Model):
  user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='profile') 
  image = models.ImageField(upload_to='users/%Y/%m/%d/',blank = True,null = True, verbose_name='фото')
  bio = models.TextField(blank=True)
  
  def __str__(self):
    return self.user.username