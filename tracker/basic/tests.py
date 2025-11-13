import uuid
from datetime import timedelta

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import transaction
from basic.models import Habit, HabitStatus, GeneralGoal, TemporalGoal
from .service.general_service import StatsService, StatsFormatter
from .service.goal_service import GoalService
from .service.habit_service import HabitService
from .views import Habits


class UseGeneralServiceTest(TestCase):
    def tearDown(self):
        """Очистка после КАЖДОГО теста"""
        try:
            with transaction.atomic():
                HabitStatus.objects.all().delete()
                Habit.objects.all().delete()
                get_user_model().objects.all().delete()
        except Exception:
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

    def test_stats_habits(self):
        """Мы создаем 3 привычки как бы выполняем их 3 дня и должно быть today_progress 3/3
        total_progress 9/9"""
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        today = timezone.now().date()
        user = get_user_model().objects.create_user(username)
        habit1 = Habit.objects.create(user=user, name="Привычка 1")
        habit2 = Habit.objects.create(user=user, name="Привычка 2")
        habit3 = Habit.objects.create(user=user, name="Привычка 3")  # ← добавил 3-ю привычку
        # Создаем выполнение за 3 дня (включая сегодня)
        dates = [today - timezone.timedelta(days=i) for i in range(3)]  # [0, -1, -2] дней
        for date in dates:
            HabitStatus.objects.create(habit=habit1, date=date, is_completed=True)
            HabitStatus.objects.create(habit=habit2, date=date, is_completed=True)
            HabitStatus.objects.create(habit=habit3, date=date, is_completed=True)  # ← 3-я привычка
        stats = StatsService.get_all_user_stats(user)
        self.assertEqual(stats['today_progress']['completed'], 3)
        self.assertEqual(stats['today_progress']['total'], 3)
        self.assertEqual(stats['today_progress']['percentage'], 100)
        self.assertEqual(stats['today_progress']['text'], '3/3')
        self.assertEqual(stats['total_progress']['completed'], 9)
        self.assertEqual(stats['total_progress']['total'], 9)
        self.assertEqual(stats['total_progress']['percentage'], 100)
        self.assertEqual(stats['total_progress']['text'], '9/9')

    def test_progress_of_goals(self):
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

    def test_stats_habits_imperfect(self):
        """Тест статистики с неидеальным выполнением"""
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        today = timezone.now().date()
        user = get_user_model().objects.create_user(username)
        habit1 = Habit.objects.create(user=user, name="Привычка 1")
        habit2 = Habit.objects.create(user=user, name="Привычка 2")
        habit3 = Habit.objects.create(user=user, name="Привычка 3")
        # Создаем выполнение за 3 дня с пропусками
        dates = [today - timezone.timedelta(days=i) for i in range(3)]
        for i, date in enumerate(dates):
            # Всегда выполняем привычку 1
            HabitStatus.objects.create(habit=habit1, date=date, is_completed=True)
            # Привычку 2 выполняем только в первые 2 дня
            if i < 2 and i != 1:
                HabitStatus.objects.create(habit=habit2, date=date, is_completed=True)
            else:
                HabitStatus.objects.create(habit=habit2, date=date, is_completed=False)
            # Привычку 3 выполняем только вчера
            if i == 1:  # вчера
                HabitStatus.objects.create(habit=habit3, date=date, is_completed=True)
            else:
                HabitStatus.objects.create(habit=habit3, date=date, is_completed=False)
        stats = StatsService.get_all_user_stats(user)
        # Проверяем неидеальную статистику:
        # Сегодня: выполнено 2 из 3 привычек
        self.assertEqual(stats['today_progress']['completed'], 2)
        self.assertEqual(stats['today_progress']['total'], 3)
        self.assertEqual(stats['today_progress']['text'], '2/3')
        # Всего: 6 выполнено из 9 возможных
        self.assertEqual(stats['total_progress']['completed'], 5)
        self.assertEqual(stats['total_progress']['total'], 9)
        self.assertEqual(stats['total_progress']['text'], '5/9')
        # Стрик: 0 (Вчера не все выполнено)
        self.assertEqual(stats['streak'], 0)
    def test_format_today(self):
        test_stats = {'today_completed': 3, 'today_total': 3} # сегодня все выполнили
        result = StatsFormatter.format_today(test_stats)
        self.assertEqual(result['percentage'], 100) # процент выполнения 100
        self.assertEqual(result['text'], '3/3') # текст прогресса все n/n
        test_stats = {'today_completed': 1, 'today_total': 3} # выполнили только 1 из 3
        result = StatsFormatter.format_today(test_stats)
        self.assertEqual(result['percentage'], 33) # процент 33 ведь 1 из 3
        self.assertEqual(result['text'], '1/3') # прогресс 1/3
    def test_format_total(self):
        test_stats = {'total_completed': 50, 'total_all': 50} # все дни мы все выполнили
        result = StatsFormatter.format_total(test_stats)
        self.assertEqual(result['percentage'], 100) # ожидаем 100% ведь все выполнили
        self.assertEqual(result['text'], '50/50') # прогресс 50/50
        test_stats = {'total_completed': 60, 'total_all': 100} # выполнили только 60 из 100
        result = StatsFormatter.format_total(test_stats)
        self.assertEqual(result['percentage'], 60) # ожидаем процент 60, ибо выполнили на 60%
        self.assertEqual(result['text'],'60/100') # ожидаем 60/100, ведь выполнили только 60 из 100

class UseHabitServiceTest(TestCase):
    def tearDown(self):
        """Очистка после КАЖДОГО теста"""
        try:
            with transaction.atomic():
                HabitStatus.objects.all().delete()
                Habit.objects.all().delete()
                get_user_model().objects.all().delete()
        except Exception:
            pass
    def test_ensure_habit_statuses_exist(self):
        """Тест создания всех нужных статусов"""
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        today = timezone.now().date()
        user = get_user_model().objects.create_user(username)
        habit1 = Habit.objects.create(user = user,name = 'Habit 1', created_at=timezone.now().date() - timedelta(days = 2)) # по сути должно быть 3 статуса
        habit2 = Habit.objects.create(user = user, name = 'Habit 2', created_at=timezone.now().date() - timedelta(days = 5)) # 6
        HabitService.ensure_habit_statuses_exist(user, timezone.now().date())
        self.assertEqual(HabitStatus.objects.all().count(), 9)

    def test_stats_of_habits(self):
        """Тест получения статистики"""
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        today = timezone.now().date()
        user = get_user_model().objects.create_user(username)
        habit1 = Habit.objects.create(user = user, name = 'Habit 1', created_at=timezone.now().date() - timedelta(days = 4))
        # 3 статуса false
        HabitStatus.objects.create(habit=habit1, date=today - timedelta(days = 4), is_completed=False)
        HabitStatus.objects.create(habit=habit1, date=today - timedelta(days = 3), is_completed=False)
        HabitStatus.objects.create(habit=habit1, date=today - timedelta(days = 2), is_completed=False)
        HabitStatus.objects.create(habit=habit1, date=today - timedelta(days = 1), is_completed=True)
        HabitStatus.objects.create(habit=habit1, date=today, is_completed=True)
        #два выполненных статуса
        habits = HabitService.get_user_habits_with_full_stats(user, today)
        habit_with_stats = habits[0]
        self.assertEqual(habit_with_stats.total_days, 5) # все дни 5
        self.assertEqual(habit_with_stats.completed_days, 2) # выполненные 2
        self.assertEqual(habit_with_stats.progress, 40) # прогресс 2/5 40%
    def test_swith_status(self):
        username = f'testuser_{uuid.uuid4().hex[:8]}'
        user = get_user_model().objects.create_user(username)
        habit1 = Habit.objects.create(user=user, name='Habit 1', created_at=timezone.now().date() - timedelta(days=4))
        status = HabitStatus.objects.create(habit=habit1, date=timezone.now().date(), is_completed=False)
        HabitService.toggle_status(status) # меняет значения статуса
        self.assertEqual(status.is_completed, True)
        status2 = HabitStatus.objects.create(habit=habit1, date=timezone.now().date() - timedelta(days = 1)
                                             ,is_completed=True)
        HabitService.toggle_status(status2)
        self.assertEqual(status2.is_completed, False)
