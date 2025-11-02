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