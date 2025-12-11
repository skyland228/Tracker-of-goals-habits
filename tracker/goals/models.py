from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

class TemporalGoal(models.Model):
    name = models.CharField(max_length=50,verbose_name='Название')
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='temporal_goals', null=True, verbose_name='Пользователь')
    deadline = models.DateField(blank = True, default='1999-11-22')  # Обязательное поле срока выполнения
    is_completed = models.BooleanField(default=False)  # Добавляем поле is_completed
    general_goal = models.ForeignKey("GeneralGoal",on_delete = models.SET_NULL,
                                     related_name='temporal_goal', null=True,
                                     blank=True, verbose_name='Основная цель')
    objects = models.Manager()
    class Meta:
        ordering = ['deadline']
        verbose_name = 'Временные цели'
        verbose_name_plural = 'Временные цели'
        
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("temporal_goal_detail", kwargs={"pk": self.pk})
    

class GeneralGoal(models.Model):
    name =  models.CharField(max_length=50,verbose_name='Название')
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='general_goals', null=True, verbose_name='Пользователь', )
    is_completed = models.BooleanField(default=False)  # Добавляем поле is_completed
    main_goal = models.OneToOneField('TemporalGoal',on_delete=models.SET_NULL, null = True, blank=True,
                                     related_name='is_main_for', verbose_name='Главная подцель')
    theme = models.ForeignKey('core.Theme', on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()

    def completed_goals(self):
        return self.temporal_goal.filter(is_completed=True)
    def incomplete_goals(self):
        return self.temporal_goal.filter(is_completed=False)
    class Meta:
        ordering = ['name']
        verbose_name = 'Основные цели'
        verbose_name_plural = 'Основные цели'
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse("general_goals_detail", kwargs={"pk": self.pk})
    