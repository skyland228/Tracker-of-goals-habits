from django.db import models

class Theme(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default="#0D20CC")  # для цвета в интерфейсе
    icon = models.CharField(max_length=50, blank=True)  # для иконки

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'