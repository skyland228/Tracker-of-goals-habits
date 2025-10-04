import datetime
from datetime import datetime, date,  timedelta
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView, DeleteView
from .forms import HabitStatusForm, AddHabit, AddTgoal
from .models import Habit, GeneralGoal, TemporalGoal, HabitStatus
from django.utils import timezone

def get_habits_with_stats(request):
    # 1. Получаем привычки пользователя
    today = date.today()
    habits_with_stats = []
    if request.user.is_authenticated:
        habits = Habit.objects.filter(user=request.user)

        # 2. Для каждой привычки создаём недостающие статусы
        for habit in habits:
            start_date = habit.created_at
            current_date = start_date

            while current_date <= today:
                HabitStatus.objects.get_or_create(
                    habit=habit,
                    date=current_date,
                    defaults={'is_completed': False}
                )
                current_date += timedelta(days=1)

        # 3. Теперь аннотируем с готовыми статусами
        habits_with_stats = habits.annotate(
            total_days=Count('habit_statuses'),
            completed_days=Count('habit_statuses', filter=Q(habit_statuses__is_completed=True))
        )

        # 4. Добавляем прогресс для каждой привычки
        for habit in habits_with_stats:
            habit.progress = (habit.completed_days / habit.total_days * 100) if habit.total_days > 0 else 0
        return habits_with_stats, today

def home(request):
    get_habits_with_stats(request)
    return render(request, 'basic/home.html', )

class Profile(TemplateView):
    template_name = 'basic/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  # Добавляем пользователя в контекст
        user = self.request.user #получаем нашего пользователя и в переменную
        today = timezone.now().date() # Определяем сегодняшнюю дату
        # ВСЕГДА пересчитываем streak из истории
        streak = self.calculate_streak_simple(user)

        # Обновляем значение в базе
        user.streak = streak
        user.save()
        today_statuses = HabitStatus.objects.filter( # получаем статус выполнения за сегодня
            habit__user=user,  # статусы привычек этого пользователя
            date=today         # только за сегодня
        )

        today_completed = today_statuses.filter(is_completed=True).count() # считаем сколько выполнено за сегодня
        today_total = today_statuses.count() # считаем сколько вообще задач за сегодня
        all_statuses = HabitStatus.objects.filter(habit__user=user) # считаем все статусы определенного пользователя
        total_completed = all_statuses.filter(is_completed=True).count() # общее кол-во выполненных задач
        total_all = all_statuses.count() # считаем общее кол-во задач
        today_percentage = round((today_completed / today_total * 100)) if today_total > 0 else 0 # высчитываем процент этого дня
        total_percentage = round((total_completed / total_all * 100)) if total_all > 0 else 0 # высчитываем процент вообще

        # Добавляем в контекст
        context['today_progress'] = {
            'completed': today_completed,
            'total': today_total,
            'text': f"{today_completed}/{today_total}",
            'percentage': today_percentage,
            'width': today_percentage  # для ширины прогресс-бара
        }

        context['total_progress'] = {
            'completed': total_completed,
            'total': total_all,
            'text': f"{total_completed}/{total_all}",
            'percentage': total_percentage,
            'width': total_percentage  # для ширины прогресс-бара
        }
        context['streak'] = user.streak
        return context

    def calculate_streak_simple(self, user):
        dates = HabitStatus.objects.filter(habit__user=user) \
            .values_list('date', flat=True).distinct().order_by('-date')
        current_date = timezone.now().date()
        streak = 0

        for data in dates:
            if isinstance(data, datetime):
                data = data.date()

            day_statuses = HabitStatus.objects.filter(habit__user=user, date=data)
            total = day_statuses.count()
            completed = day_statuses.filter(is_completed=True).count()

            # Если дата = сегодня
            if data == current_date:
                if total > 0 and total == completed:
                    streak += 1
                    current_date -= timezone.timedelta(days=1)
                else:
                    # Сегодня ещё не всё сделано → streak не ломаем
                    continue

            elif data == current_date - timezone.timedelta(days=1):
                if total > 0 and total == completed:
                    streak += 1
                    current_date -= timezone.timedelta(days=1)
                else:
                    break

            else:
                # если дата "прыгает" через день или раньше → streak рвётся
                break
        return streak

class AddHabits(CreateView):
    model = Habit
    template_name = 'basic/add_habit.html'
    success_url = reverse_lazy('habits')
    form_class = AddHabit

    def form_valid(self, form):
        form.instance.user = self.request.user  #устанавливаем пользователя
        return super().form_valid(form)

class DeleteHabit(LoginRequiredMixin, DeleteView):
    model = Habit
    success_url = reverse_lazy('habits')
    template_name = 'basic/habit_delete.html'
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

class UpdateHabit(LoginRequiredMixin, UpdateView):
    model = Habit
    success_url = reverse_lazy('habits')
    template_name = 'basic/add_habit.html'
    fields = ['name','goal']
    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

class AddTemporalGoal(LoginRequiredMixin,CreateView):
    model = TemporalGoal
    template_name = 'basic/add_temporal_goal.html'
    success_url = reverse_lazy('temporal_goals')
    form_class = AddTgoal

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteTemporalGoal(LoginRequiredMixin,DeleteView):
    model = TemporalGoal
    success_url = reverse_lazy('temporal_goals')
    template_name = 'basic/temporal_goal_delete.html'

class UpdateTemporalGoal(LoginRequiredMixin, UpdateView):
    mdoel = TemporalGoal
    success_url = reverse_lazy('temporal_goals')
    template_name = 'basic/add_temporal_goal.html'
    fields = ['name','general_goal','deadline']
    def get_queryset(self):
        return TemporalGoal.objects.filter(user=self.request.user)


class Habits(LoginRequiredMixin,ListView):
    model = Habit
    template_name = 'basic/Habits.html'
    context_object_name = 'habits'
    paginate_by = 5
    login_url = 'users:login'
    def get_queryset(self):
        today = date.today()
        user_habits = Habit.objects.filter(user=self.request.user)
        for habit in user_habits:
            HabitStatus.objects.get_or_create(habit=habit, date=today)
        habits = user_habits.prefetch_related('habit_statuses').annotate(
            total_days = Count('habit_statuses'),
            completed_days=Count('habit_statuses',filter=(Q(habit_statuses__is_completed=True))))
        for habit in habits:
            habit.progress = (habit.completed_days / habit.total_days * 100) if habit.total_days > 0 else 0
        return habits

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()

        # Добавляем текущий статус для каждой привычки
        for habit in context['habits']:
            habit.today_status = habit.habit_statuses.filter(date=today).first()

        return context


class HabitStatusUpdateView(UpdateView):
    model = HabitStatus
    form_class = HabitStatusForm

    def form_valid(self, form):
        # Получаем текущий объект из базы, а не из формы
        status = self.get_object()
        status.is_completed = not status.is_completed
        status.save()
        return redirect('habits')

class GeneralGoals(LoginRequiredMixin,ListView):
    model = GeneralGoal
    template_name = 'basic/general_goal.html'
    context_object_name = 'goals'
    login_url = 'users:login'
    def get_queryset(self):
        return GeneralGoal.objects.filter(user=self.request.user)

class TemporalGoals(LoginRequiredMixin,ListView):
    model = TemporalGoal
    template_name = 'basic/temporal_goal.html'
    context_object_name = 'goals'
    login_url = 'users:login'
    def get_queryset(self):
        return TemporalGoal.objects.filter(user=self.request.user)

class TemporalGoalCheck(LoginRequiredMixin, View):
    def post(self,request,pk):
        goal = get_object_or_404(TemporalGoal,pk = pk, user=request.user)

        goal.is_completed = not goal.is_completed
        goal.save()
        return redirect('temporal_goals')

class TemporalGoalDetail(LoginRequiredMixin, DetailView):
    model = TemporalGoal
    template_name = 'basic/temporal_goal_detail.html'
    context_object_name = 'goal'

    def get_queryset(self):
        # Только цели текущего пользователя
        return TemporalGoal.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        temporal_goal = self.object  # Это наша временная цель

        # Получаем общую цель
        general_goal = temporal_goal.general_goal

        # ★ ПРАВИЛЬНО: получаем все привычки через временные цели этой общей цели ★
        habits = Habit.objects.filter(
            goal__general_goal=general_goal,  # Привычки, связанные с временными целями этой общей цели
            user=self.request.user  # Только привычки текущего пользователя
        ).select_related('goal')  # Оптимизация запросов

        # Добавляем в контекст
        context['general_goal'] = general_goal
        context['habits'] = habits

        return context
