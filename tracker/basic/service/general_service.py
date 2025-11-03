from django.db.models import Count, Q
from django.utils import timezone
from ..models import HabitStatus

class StatsService:
    @staticmethod
    def calculate_streak_simple(user):
        dates = HabitStatus.objects.filter(habit__user=user) \
            .values_list('date', flat=True).distinct().order_by('-date') # получаем наши статусы за дни
        all_statuses = HabitStatus.objects.filter(
            habit__user=user,
            date__in=dates  # все интересующие нас даты
        ).values('date').annotate(
            total=Count('id'),
            completed=Count('id', filter=Q(is_completed=True)))
        current_date = timezone.now().date() # получаем текущию дату
        streak = 0
        stats_by_date = {item['date']: item for item in all_statuses}
        for data in dates:
            stats = stats_by_date.get(data, {'total': 0, 'completed': 0})
            total = stats['total']
            completed = stats['completed']
            if data == current_date: # Если дата = сегодня
                if total > 0 and total == completed: # если все привычки сегодня уже выполнены
                    streak += 1
                    current_date -= timezone.timedelta(days=1) # это был сегодня все сделали значит день минус
                else: # Сегодня ещё не всё сделано → streak не ломаем
                    continue
            elif data == current_date - timezone.timedelta(days=1):  # проверка на последовательные дни
                if total > 0 and total == completed:
                    streak += 1
                    current_date -= timezone.timedelta(days=1)
                else:
                    break
            else:
                break # ну если последовательности нет то рвем стрик
        return streak

    @staticmethod
    def get_all_user_stats(user):
        today = timezone.now().date()
        stats = HabitStatus.objects.filter(habit__user = user).aggregate( # получаем данные одним запросом
            today_total = Count('id', filter = Q(date=today)), # Общее кол-во сегодня
            today_completed = Count('id', filter = Q(date=today, is_completed = True)), # Выполненные сегодня
            total_all = Count('id'), # общее кол-во вообще
            total_completed = Count('id', filter = Q(is_completed = True)),)# выполненные вообще
        streak = StatsService.calculate_streak_simple(user)
        return {
            'today_progress': StatsFormatter.format_today(stats),
            'total_progress': StatsFormatter.format_total(stats),
            'streak': streak }

class StatsFormatter:
    @staticmethod
    def format_today(stats):
        completed = stats['today_completed'] or 0
        total = stats['today_total'] or 0
        percentage = round((completed / total) * 100) if total > 0 else 0
        return {
            'completed': completed,
            'total': total,
            'percentage': percentage,
            'text': f"{completed}/{total}"}
    @staticmethod
    def format_total(stats):
        completed = stats['total_completed'] or 0
        total = stats['total_all'] or 0
        percentage = round((completed / total) * 100) if total > 0 else 0
        return {
            'completed': completed,
            'total': total,
            'percentage': percentage,
            'text': f"{completed}/{total}"
        }
