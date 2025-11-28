from datetime import timedelta
import uuid
from django.utils import timezone
from django.test import TestCase
from .models import Habit, HabitStatus
from .services.habit_service import HabitServices
from django.contrib.auth import get_user_model

class UseHabitServiceTest(TestCase):
    def test_ensure_habit_statuses_exist(self):
        """Тест создания всех нужных статусов"""
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        today = timezone.now().date()
        user = get_user_model().objects.create_user(username)
        habit1 = Habit.objects.create(user = user,name = 'Habit 1', created_at=timezone.now().date() - timedelta(days = 2)) # по сути должно быть 3 статуса
        habit2 = Habit.objects.create(user = user, name = 'Habit 2', created_at=timezone.now().date() - timedelta(days = 5)) # 6
        HabitServices.ensure_habit_statuses_exist(user, timezone.now().date())
        self.assertEqual(HabitStatus.objects.all().count(), 9)
