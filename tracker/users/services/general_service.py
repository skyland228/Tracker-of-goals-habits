from django.db.models import Count, Q
from django.utils import timezone
from habits.models import HabitStatus

class StatsService:
    @staticmethod
    def calculate_stats(user): # получается здесь мы вычисляем стрик когда выполняем все привычки без пропуска
        all_statuses = HabitStatus.objects.filter( habit__user = user).values(
            'date').order_by('-date').annotate(
        # и вот тут уже мы начинаем добавлять поля
        total=Count('id'),
        completed = Count('id', filter=Q(is_completed = True))
        ) 
        streak = 0
        today = timezone.localdate()
        for stat in all_statuses:
            date = stat['date']
            total = stat['total']
            completed = stat['completed']
            if date == today:
                if total > 0 and total == completed:
                    streak +=1
                else:
                    continue
            if date != today:
                if total > 0 and total == completed:
                    streak += 1
                else: 
                    break
        reversed_statuses = all_statuses[::-1]  # [::-1] переворачивает список
        current_streak = 0
        max_streak = 0
        for stat in reversed_statuses:
            date = stat['date']
            total = stat['total']
            completed = stat['completed']
            if total > 0 and total == completed:
                current_streak +=1
                if current_streak > max_streak:
                    max_streak = current_streak 
            else:
                current_streak = 0

        stats = HabitStatus.objects.filter(habit__user = user).aggregate(
            today_total = Count('id', filter=Q(date=today)),
            today_completed = Count('id', filter=Q(date=today, is_completed=True)),
            total_all = Count('id'), # общее кол-во вообще
            total_completed = Count('id', filter = Q(is_completed = True)))# выполненные вообще)
        total_completed_value = stats['total_completed'] or 0
        total_all_value = stats['total_all'] or 0
        percentage = round((total_completed_value / total_all_value) * 100) if total_all_value > 0 else 0
        return {
            'streak':streak,
            'today_progress':{
                'completed': stats['today_completed'],
                'total': stats['today_total']  },
            'total_progress':{
                'completed': total_completed_value,
                'total': total_all_value,
                'percentage': percentage,
            },'max_streak': max_streak}
