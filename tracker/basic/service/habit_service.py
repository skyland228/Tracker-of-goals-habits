from datetime import timedelta
from django.core.cache import cache
from django.db.models import Count, Q
from django.utils import timezone
from ..models import Habit, HabitStatus

class HabitService:
    @staticmethod
    def ensure_habit_statuses_exist(user, target_date=None):
        """Создает недостающие статусы для привычек пользователя"""
        if target_date is None:
            target_date = timezone.now().date()
        habits = Habit.objects.filter(user=user)
        # ОДИН запрос - получить все существующие статусы для всех привычек пользователя
        all_existing_statuses = HabitStatus.objects.filter(
            habit__user=user
        ).values('habit_id', 'date')
        existing_dates_by_habit = {}
        for status in all_existing_statuses:
            habit_id = status['habit_id'] # выбираен нашу привычку по id
            date = status['date'] # получаем дату этой привычки
            if habit_id not in existing_dates_by_habit: # проверяем, если еще нет места для статуса этой привычуки
                existing_dates_by_habit[habit_id] = set() # создаем место для такой привывчки
            existing_dates_by_habit[habit_id].add(date) # добавляем нашу дату статуса в место привычки
        statuses_to_create = [] # создаем список для добавления привычек, чтобы потом за 1 запрос
        for habit in habits:
            # Берем существующие даты из словаря (пустой set если нет статусов)
            existing_dates = existing_dates_by_habit.get(habit.id, set())
            start_date = habit.created_at # фиксируем дату создания
            end_date = timezone.now().date()  # дата последнего статуса понятно, что сегодня
            current_date = start_date # наша текущая дата начинается со дня создания
            while current_date <= end_date: # пока наша текущая дата меньше конечной
                if current_date not in existing_dates: # если не сущ статуса по такой дате
                    # Создаем статус пока добавляя его в наш список
                    statuses_to_create.append(
                        HabitStatus(habit=habit, date=current_date, is_completed=False))
                    current_date = current_date + timedelta(days=1) # ну меняем тек дату на день
            if statuses_to_create: # если список не пустой и есть привычки, которым надо создать статус
                HabitStatus.objects.bulk_create(statuses_to_create, batch_size=100) # то создаем привычки из списка
                # по 100 штук за раз
    @staticmethod
    def get_user_habits_with_progress(user,date =None):
        """Возращяет прогресс привычек"""
        if date is None:
            date = timezone.now().date()
        HabitService.ensure_habit_statuses_exist(user, date)
        habits = Habit.objects.filter(user=user).annotate(
            total_days = Count('habit_statuses'),
            completed_days = Count('habit_statuses', filter=Q(habit_statuses__is_completed=True)))
        return [{
                'habit': habit,
                'total_days': habit.total_days,
                'completed_days': habit.completed_days }
            for habit in habits ]

    @staticmethod
    def get_habits_with_today_status(user, today):
        habits = Habit.objects.filter(user=user) # получаем привычки нашего пользователя
        habit_ids = [habit.id for habit in habits] # вычисляем все id наших привычек
        today_statuses = HabitStatus.objects.filter(
            habit_id__in=habit_ids,
            date=today) # получаем сегодняшний статус для привычек
        status_by_habit_id = {status.habit_id: status for status in today_statuses} # создаем словарь
        # где каждой нашей привычки соответствует id
        statuses_to_create = []
        for habit in habits:
            if habit.id not in status_by_habit_id:
                new_status = HabitStatus(habit = habit, date=today, is_completed=False)
                statuses_to_create.append(new_status) # отмечаем в списке статус
                habit.today_status = new_status
            else:
                habit.today_status = status_by_habit_id.get(habit.id) # ну и получаем статус для каждой привычки
        if statuses_to_create:
            HabitStatus.objects.bulk_create(statuses_to_create) # создаем записи статусов в бд
        return habits
    @staticmethod
    def get_user_habits_with_full_stats(user, date=None):
        if date is None:
            date = timezone.now().date()
        # ТОЛЬКО ОДИН запрос - он уже создаст статусы и вернет статистику
        habits_data = HabitService.get_user_habits_with_progress(user, date)
        # Преобразуем в удобный формат
        result = []
        for item in habits_data:
            habit = item['habit']
            habit.total_days = item['total_days']
            habit.completed_days = item['completed_days']
            habit.progress = (item['completed_days'] / item['total_days'] * 100) if item['total_days'] > 0 else 0
            habit.today_status = habit.habit_statuses.filter(date=date).first()
            result.append(habit)
        return result

    @staticmethod
    def toggle_status(status):
        status.is_completed = not status.is_completed
        status.save()
