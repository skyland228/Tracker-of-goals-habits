from django.contrib.auth import get_user_model
from django.db import models

class TemporalGoal(models.Model):
    name = models.CharField(max_length=50)
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
    def __str__(self):
        return self.name

class GeneralGoal(models.Model):
    name =  models.CharField(max_length=50)
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
    def __str__(self):
        return self.name