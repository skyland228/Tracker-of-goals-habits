from django.db import models
from datetime import date
from django.contrib.auth import get_user_model
from basic.models import TemporalGoal

class Habit(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(
        get_user_model(),on_delete=models.SET_NULL,related_name='habits',null=True,verbose_name='Пользователь',)
    created_at = models.DateField(default=date.today)
    goal = models.ForeignKey(TemporalGoal,on_delete=models.SET_NULL,
                             related_name='habits', null = True, blank = True,
                             verbose_name='Цель') # мы записываем, какой цели следует эта привычка
    objects = models.Manager()
    class Meta:
        ordering = ['-created_at']
        app_label = 'habits'
    def __str__(self):
        return self.name

class HabitStatus(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='habit_statuses')
    is_completed = models.BooleanField(default=False)
    date = models.DateField(default=date.today)

    objects = models.Manager()
    class Meta:
        unique_together = ('habit', 'date')
        app_label = 'habits'
    def __str__(self):
        return self.habit.name