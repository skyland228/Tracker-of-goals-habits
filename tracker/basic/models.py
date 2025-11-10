from django.contrib.auth import get_user_model
from django.db import models
from datetime import date
from django.utils import timezone


class Habit(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        get_user_model(),on_delete=models.SET_NULL,related_name='habits',null=True,verbose_name='Пользователь',)
    created_at = models.DateField(default=date.today)
    goal = models.ForeignKey('TemporalGoal',on_delete=models.SET_NULL,
                             related_name='habits', null = True, blank = True,
                             verbose_name='Цель') # мы записываем, какой цели следует эта привычка
    objects = models.Manager()
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.name

class HabitStatus(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='habit_statuses')
    is_completed = models.BooleanField(default=False)
    date = models.DateField(default=date.today)

    objects = models.Manager()
    class Meta:
        unique_together = ('habit', 'date')
    def __str__(self):
        return self.habit.name

class Theme(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, default='#000000')  # для цвета в интерфейсе
    icon = models.CharField(max_length=50, blank=True)  # для иконки

    def __str__(self):
        return self.name


class GeneralGoal(models.Model):
    name =  models.CharField(max_length=50)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='general_goals', null=True, verbose_name='Пользователь', )
    is_completed = models.BooleanField(default=False)  # Добавляем поле is_completed
    theme = models.ForeignKey(Theme, on_delete=models.SET_NULL, null=True, blank=True)
    objects = models.Manager()

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class TemporalGoal(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    user = models.ForeignKey(
        get_user_model(), on_delete=models.SET_NULL,
        related_name='temporal_goals', null=True, verbose_name='Пользователь')
    deadline = models.DateField(blank = True, default='1999-11-22')  # Обязательное поле срока выполнения
    is_completed = models.BooleanField(default=False)  # Добавляем поле is_completed
    general_goal = models.ForeignKey(GeneralGoal,on_delete = models.SET_NULL,
                                     related_name='temporal_goal', null=True,
                                     blank=True, verbose_name='Основная цель')
    objects = models.Manager()

    class Meta:
        ordering = ['deadline']
    def __str__(self):
        return self.name

