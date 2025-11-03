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
from .service.general_service import StatsService
from .service.habit_service import HabitService


def home(request):
    return render(request, 'basic/home.html', )

class Profile(TemplateView):
    template_name = 'basic/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = StatsService.get_all_user_stats(self.request.user)
        context.update({
            'user': self.request.user,
            'today_progress': stats['today_progress'],
            # 'total_progress': stats['total_progress'],  # потом раскомментируешь
            # 'streak': stats['streak']  # потом раскомментируешь
        })
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
    model = TemporalGoal
    success_url = reverse_lazy('temporal_goals')
    template_name = 'basic/add_temporal_goal.html'
    fields = ['name','general_goal','deadline']
    def get_queryset(self):
        return TemporalGoal.objects.filter(user=self.request.user)


class Habits(LoginRequiredMixin, ListView):
    model = Habit
    template_name = 'basic/Habits.html'
    context_object_name = 'habits'
    paginate_by = 5
    login_url = 'users:login'

    def get_queryset(self):
        habits_data = HabitService.get_user_habits_with_progress(self.request.user)

        # Добавляем прогресс и превращаем в объекты
        habits = []
        for item in habits_data:
            habit = item['habit']
            habit.total_days = item['total_days']
            habit.completed_days = item['completed_days']
            habit.progress = (item['completed_days'] / item['total_days'] * 100) if item['total_days'] > 0 else 0
            habits.append(habit)

        return habits

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = date.today()

        for habit in context['habits']:
            habit.today_status = habit.habit_statuses.filter(date=today).first()
            # Если статуса нет - создаем
            if not habit.today_status:
                habit.today_status = HabitStatus.objects.create(
                    habit=habit,
                    date=today,
                    is_completed=False
                )

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
