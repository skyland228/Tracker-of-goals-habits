from django.db.models import Count, Q
from django.utils import timezone
from ..models import HabitStatus

class StatsService:
    @staticmethod
    def get_all_user_stats(user):
        today = timezone.now().date()
        stats = HabitStatus.objects.filter(habit__user = user).aggregate( # получаем данные одним запросом
            today_total = Count('id', filter = Q(date=today)), # Общее кол-во сегодня
            today_completed = Count('id', filter = Q(date=today, is_completed = True)), # Выполненные сегодня
            total_all = Count('id'), # общее кол-во вообще
            total_completed = Count('id', filter = Q(is_completed = True)),)# выполненные вообще
        return {
            'today_progress': StatsFormatter.format_today(stats),
            'total_progress': StatsFormatter.format_total(stats),
        }

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
# class ProfileService:
#     @staticmethod
#     def get_today_progress(user):
#         today = timezone.now().date()
#         today_statuses = HabitStatus.objects.filter(#  мы получаем статус на сегодня по нашему пользователю
#             habit_user = user,
#             date = today,
#         )

    # def get_context_data(self, **kwargs):
    # context = super().get_context_data(**kwargs)
    # context['user'] = self.request.user  # Добавляем пользователя в контекст
    # user = self.request.user #получаем нашего пользователя и в переменную
    # today = timezone.now().date() # Определяем сегодняшнюю дату
    # # ВСЕГДА пересчитываем streak из истории
    # streak = self.calculate_streak_simple(user)
    #
    # # Обновляем значение в базе
    # user.streak = streak
    # user.save()
    # today_statuses = HabitStatus.objects.filter( # получаем статус выполнения за сегодня
    #     habit__user=user,  # статусы привычек этого пользователя
    #     date=today         # только за сегодня
    # )
    #     today_completed = today_statuses.filter(is_completed=True).count() # считаем сколько выполнено за сегодня
    #     today_total = today_statuses.count() # считаем сколько вообще задач за сегодня
    #     all_statuses = HabitStatus.objects.filter(habit__user=user) # считаем все статусы определенного пользователя
    #     total_completed = all_statuses.filter(is_completed=True).count() # общее кол-во выполненных задач
    #     total_all = all_statuses.count() # считаем общее кол-во задач
    # today_percentage = round((today_completed / today_total * 100)) if today_total > 0 else 0 # высчитываем процент этого дня
    # total_percentage = round((total_completed / total_all * 100)) if total_all > 0 else 0 # высчитываем процент вообще
    #
    # # Добавляем в контекст
    # context['today_progress'] = {
    #     'completed': today_completed,
    #     'total': today_total,
    #     'text': f"{today_completed}/{today_total}",
    #     'percentage': today_percentage,
    #     'width': today_percentage  # для ширины прогресс-бара
    # }
    #
    # context['total_progress'] = {
    #     'completed': total_completed,
    #     'total': total_all,
    #     'text': f"{total_completed}/{total_all}",
    #     'percentage': total_percentage,
    #     'width': total_percentage  # для ширины прогресс-бара
    # }
    # context['streak'] = user.streak
    # return context