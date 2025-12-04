from datetime import date, timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from habits.models import Habit, HabitStatus
from habits.services.habit_service import HabitServices

class UseHabitServicesTest(TestCase):
  def test_ensure_habit_statuses_exist(self):
    """Тест создания всех нужных статусов"""
    user = get_user_model().objects.create_user("user")
    habit1 = Habit.objects.create(user = user, name = "habit1", created_at = date.today() - timedelta(days = 2))
    habit2 = Habit.objects.create(user = user, name = "habit2", created_at = date.today() - timedelta(days = 5))
    HabitServices.ensure_habit_statuses_exist(user)
    self.assertEqual(HabitStatus.objects.all().count(), 9)
  def test_get_stats_of_habit(self):
    """Тест получения статистики"""
    user = get_user_model().objects.create_user("user")
    habit1 = Habit.objects.create(user = user, name = "habit", created_at = date.today() - timedelta(days = 4))
    HabitStatus.objects.create(habit = habit1, date = date.today() - timedelta(days = 4), is_completed = False)
    HabitStatus.objects.create(habit = habit1, date = date.today() - timedelta(days = 3), is_completed = False)
    HabitStatus.objects.create(habit = habit1, date = date.today() - timedelta(days = 2), is_completed = False)
    HabitStatus.objects.create(habit = habit1, date = date.today() - timedelta(days = 1), is_completed = True)
    HabitStatus.objects.create(habit = habit1, date = date.today(), is_completed = True)
    #два выполненных статуса
    habits = HabitServices.get_user_habit_stats(user)
    habit_with_stats = habits[0] # .first получает данные уже из кэша
    self.assertEqual(habit_with_stats.total_days, 5) # всего 5 дней
    self.assertEqual(habit_with_stats.completed_days, 2 ) # из 5 дней выполненно только 2
    self.assertEqual(habit_with_stats.habit_progress, 40) # 2 / 5 40% 
    self.assertTrue(habit_with_stats.today_status) # Сегодня привычка выполненна поэтому ее значение true

