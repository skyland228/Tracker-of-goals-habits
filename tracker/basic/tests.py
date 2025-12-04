import uuid
from datetime import timedelta
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from basic.models import  GeneralGoal, TemporalGoal
from basic.service.general_service import StatsService, StatsFormatter
from basic.service.goal_service import GoalService
from habits.models import Habit, HabitStatus

class UseGeneralServiceTest(TestCase):
    def test_streak(self): # по сути это в core
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

    def test_streak_break(self): # это тоже core
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

    def test_streak_with_today_incomplete(self): #core
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

    def test_progress_of_goals(self): # temporal_goal
        """Тест расчета прогресса цели"""
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        user = get_user_model().objects.create_user(username)
        general_goal = GeneralGoal.objects.create(user=user, name = "Главная цель")
        subgoal_1 = TemporalGoal.objects.create(user = user, name = "Подцель 1", general_goal = general_goal,
                                                is_completed = True)
        subgoal_2 = TemporalGoal.objects.create(user = user, name = "Подцель 2", general_goal = general_goal,
                                                is_completed = False)
        result = GoalService.progress_of_goal(general_goal)
        self.assertEqual(result, 50) # одну под цель я выполнил другую нет 50
        # Назначаем главную цель
        general_goal.main_goal = subgoal_1  # subgoal_1 - главная цель бонус + 20
        general_goal.save()
        result = GoalService.progress_of_goal(general_goal)
        self.assertEqual(result, 70) # уже главная цель дает бонус + 20

    