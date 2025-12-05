from datetime import timedelta
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
        completed = Count('id', filter=Q(is_completed = True))) 
        current_date = timezone.now().date() # получаем текущию дату
        streak = 0
        for stat in all_statuses:
            date = stat['date']
            total = stat['total']
            completed = stat['completed']
            if date == current_date:# сегодня
                if total > 0 and total == completed: #если все выполненно уже сегодня
                    streak +=1
                    current_date -= timedelta(days = 1)    # ну если, выполнили и день = сегодня до день уменьшаем
                # ничего не делаем день еще не кончился
            else:
                if date == current_date - timedelta(days = 1) and total > 0 and total == completed: # день раньше чем сегодня все уже нет времени выполнить, то есть или да, или рвем стрик
                    streak += 1
                    current_date -= timedelta(days = 1)
                else:
                    break
        stats = HabitStatus.objects.filter(habit__user = user).aggregate(
            today_total = Count('id', filter=Q(date = timezone.now().date())),
            today_completed = Count('id', filter=Q(date = timezone.now().date(), is_completed = True)),
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
                'percentage': percentage}}
