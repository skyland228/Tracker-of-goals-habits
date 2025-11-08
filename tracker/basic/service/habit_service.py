from datetime import timedelta
from django.core.cache import cache
from django.utils import timezone
from ..models import Habit, HabitStatus

class HabitService:
    @staticmethod
    def get_user_habits_with_progress(user, date=None):
        if date is None:
            date = timezone.now().date()
        cache_key = f'status_created_{user.id}_{date}'
        if cache.get(cache_key):
            # Если в кеше - просто возвращаем привычки
            habits = Habit.objects.filter(user=user).prefetch_related('habit_statuses')
            # Вручную считаем статистику
            habits_with_stats = []
            for habit in habits:
                total_days = habit.habit_statuses.count()
                completed_days = habit.habit_statuses.filter(is_completed=True).count()
                habits_with_stats.append({
                    'habit': habit,
                    'total_days': total_days,
                    'completed_days': completed_days
                })
            return habits_with_stats

        habits_with_stats = []
        habits = Habit.objects.filter(user=user)

        for habit in habits:
            start_date = habit.created_at
            current_date = start_date
            total_days = 0
            completed_days = 0

            while current_date <= date:
                status, created = HabitStatus.objects.get_or_create(
                    habit=habit,
                    date=current_date,
                    defaults={'is_completed': False}
                )
                total_days += 1
                if status.is_completed:
                    completed_days += 1
                current_date += timedelta(days=1)

            habits_with_stats.append({
                'habit': habit,
                'total_days': total_days,
                'completed_days': completed_days
            })

        cache.set(cache_key, True, 86400)
        return habits_with_stats

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
        # 1. Получаем привычки с today_status
        habits = HabitService.get_habits_with_today_status(user, date)
        # 2. Получаем статистику прогресса
        habits_data = HabitService.get_user_habits_with_progress(user, date)
        # 3. Создаем словарь для быстрого доступа к статистике
        stats_by_habit_id = {}
        for item in habits_data:
            stats_by_habit_id[item['habit'].id] = {
                'total_days': item['total_days'],
                'completed_days': item['completed_days']
            }
        # 4. Добавляем статистику к существующим habits
        for habit in habits:
            stats = stats_by_habit_id.get(habit.id, {'total_days': 0, 'completed_days': 0})
            habit.total_days = stats['total_days']
            habit.completed_days = stats['completed_days']
            habit.progress = (stats['completed_days'] / stats['total_days'] * 100) if stats['total_days'] > 0 else 0
        return habits
    @staticmethod
    def toggle_status(status):
        status.is_completed = not status.is_completed
        status.save()
