from datetime import timedelta
from django.db.models import Count, Q,Prefetch
from habits.models import Habit, HabitStatus
from django.utils import timezone

class HabitServices:
    """
    Рассчитывает процент выполнения глобальной цели.
    Прогресс определяется по доле выполненных временных целей.
    Если у глобальной цели указана главная подцель и она выполнена,
    к базовому прогрессу добавляется бонус 20%.
    Итоговое значение не может превышать 100.
    """
    @staticmethod
    def ensure_habit_statuses_exist(user):
        """
        Создаёт недостающие ежедневные статусы привычек пользователя.
        Для каждой привычки пользователя метод проверяет,
        есть ли записи `HabitStatus` на все даты от дня создания привычки
        до текущего дня. Если каких-то записей нет, они создаются автоматически.
        Метод изменяет данные в базе.
        """
        habits = Habit.objects.filter(user=user)
        today = timezone.localdate()
        
        all_existing_statuses = HabitStatus.objects.filter( 
            habit__user=user
        ).values('habit_id', 'date')
        
        existing_dates_by_habit = {}
        for status in all_existing_statuses:
            habit_id = status['habit_id']
            status_date = status['date']  
            if habit_id not in existing_dates_by_habit:
                existing_dates_by_habit[habit_id] = set()
            existing_dates_by_habit[habit_id].add(status_date)
        
        statuses_to_create = []
        for habit in habits:
            existing_dates = existing_dates_by_habit.get(habit.id, set())
            start_date = habit.created_at
            end_date = today 
            
            current_date = start_date
            while current_date <= end_date:
                if current_date not in existing_dates:
                    statuses_to_create.append(
                        HabitStatus(habit=habit, date=current_date, is_completed=False)
                    )
                current_date += timedelta(days=1)  
        
        if statuses_to_create:
            HabitStatus.objects.bulk_create(statuses_to_create, batch_size=100)
    @staticmethod
    def get_user_habit_stats(user):
        """
        Возвращает привычки пользователя вместе с вычисленной статистикой.

        Перед выборкой метод сначала гарантирует наличие ежедневных статусов.
        Затем для каждой привычки рассчитывает:
        - общее число дней отслеживания;
        - число выполненных дней;
        - процент выполнения;
        - статус на текущий день.

        Возвращает queryset привычек с дополнительными вычисленными полями.
        """
        today = timezone.localdate()
        HabitServices.ensure_habit_statuses_exist(user)
        habits = Habit.objects.filter(user = user).annotate(
            total_days = Count('habit_statuses'),
            completed_days = Count('habit_statuses', filter=Q(habit_statuses__is_completed=True )))\
        .prefetch_related(Prefetch('habit_statuses', queryset=HabitStatus.objects.filter(date = today), to_attr= 'today_statuses'))
        for habit in habits:
            habit.habit_progress = int((habit.completed_days / habit.total_days) * 100) if habit.total_days > 0 else 0
            habit.today_status = habit.today_statuses[0] if habit.today_statuses else None
        return habits
    @staticmethod
    def change_status(status):
        """
        Переключает статус выполнения привычки за конкретную дату.

        Меняет значение поля `is_completed` у объекта `HabitStatus`
        на противоположное и сохраняет его в базе данных.
        """
        status.is_completed = not status.is_completed
        status.save() 