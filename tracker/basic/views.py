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
            'total_progress': stats['total_progress'],
            'streak': stats['streak']})
        return context

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

class Habits(LoginRequiredMixin, ListView):  # вот это God Method
    model = Habit
    template_name = 'basic/Habits.html'
    context_object_name = 'habits'
    paginate_by = 5
    login_url = 'users:login'

    def get_queryset(self):
        return HabitService.get_user_habits_with_full_stats(self.request.user)



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

class TemporalGoalDetail(LoginRequiredMixin, DetailView): # вот это God Method
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