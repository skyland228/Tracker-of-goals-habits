import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from basic.models import Habit, HabitStatus
from .service.general_service import StatsService


class UseServiceTest(TestCase):

    def tearDown(self):
        """Очистка после КАЖДОГО теста"""
        try:
            # Пытаемся очистить в транзакции
            with transaction.atomic():
                HabitStatus.objects.all().delete()
                Habit.objects.all().delete()
                get_user_model().objects.all().delete()
        except Exception:
            # Если транзакция сломана - пропускаем очистку
            pass

    def test_streak(self):
        """Тест расчета серии при последовательном выполнении привычки 5 дней подряд"""
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        user = get_user_model().objects.create_user(username)
        habit1 = Habit.objects.create(user=user, name="Привычка 1")
        habit2 = Habit.objects.create(user=user, name="Привычка 2")

        dates = [timezone.now().date() - timezone.timedelta(days=i) for i in range(5)]
        for date in dates:
            HabitStatus.objects.create(habit=habit1, date=date, is_completed=True)
            HabitStatus.objects.create(habit=habit2, date=date, is_completed=True)
        streak = StatsService.calculate_streak_simple(user)
        self.assertEqual(streak, 5)

    def test_streak_break(self):
        """Стрик должен прерваться при пропуске ВЧЕРАШНЕГО дня"""
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        user = get_user_model().objects.create_user(username)
        habit1 = Habit.objects.create(user=user, name="Привычка BREAK 1")
        habit2 = Habit.objects.create(user=user, name="Привычка BREAK 2")
        # Создаем выполнение 3 дня подряд (дни: -4, -3, -2)
        dates = [timezone.now().date() - timezone.timedelta(days=i) for i in range(3, 1, -1)]
        for date in dates:
            HabitStatus.objects.create(habit=habit1, date=date, is_completed=True)
            HabitStatus.objects.create(habit=habit2, date=date, is_completed=True)
        # ВЧЕРА (день -1) - НЕ ВЫПОЛНЕНО (пропуск)
        # СЕГОДНЯ (день 0) - выполняем
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        streak = StatsService.calculate_streak_simple(user)
        self.assertEqual(streak, 0)  # Стрик должен быть 0 из-за пропуска вчера

    def test_streak_with_today_incomplete(self):
        """Проверяем как ведет себя стрик, когда сегодня выполнены не все привычки"""
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        user = get_user_model().objects.create_user(username)
        habit1 = Habit.objects.create(user=user, name="Привычка 1")
        habit2 = Habit.objects.create(user=user, name="Привычка 2")
        # Вчера выполнили ВСЕ привычки streak = 1
        yesterday = timezone.now().date() - timezone.timedelta(days=1)
        HabitStatus.objects.create(habit=habit1, date=yesterday, is_completed=True)
        HabitStatus.objects.create(habit=habit2, date=yesterday, is_completed=True)
        # Сегодня выполнили только ОДНУ из двух привычек
        today = timezone.now().date()
        HabitStatus.objects.create(habit=habit1, date=today, is_completed=True)  # выполнена
        HabitStatus.objects.create(habit=habit2, date=today, is_completed=False)  # НЕ выполнена
        streak = StatsService.calculate_streak_simple(user)
        # Ожидаем: стрик = 1, так как сегодня выполнены не все привычки
        self.assertEqual(streak, 1)