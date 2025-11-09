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
from .Mixin import UserObjectsMixin
from .forms import HabitStatusForm, AddHabit, AddTgoal, AddGeneralGoal, CreateTheme
from .models import Habit, GeneralGoal, TemporalGoal, HabitStatus, Theme
from django.utils import timezone
from .service.general_service import StatsService
from .service.habit_service import HabitService
from .service.goal_service import GoalService

def home(request):
    return render(request, 'basic/core/home.html', )

class Profile(TemplateView):
    template_name = 'basic/core/profile.html'
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
    template_name = 'basic/habit/add_habit.html'
    success_url = reverse_lazy('habits')
    form_class = AddHabit

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)  # ← сначала СОХРАНЯЕМ привычку
        HabitService.get_habits_with_today_status(self.request.user, today=timezone.now())
        # HabitService.ensure_habit_statuses_exist(self.request.user)  # ← теперь создаст статусы
        return response

class DeleteHabit(UserObjectsMixin,LoginRequiredMixin, DeleteView):
    model = Habit
    success_url = reverse_lazy('habits')
    template_name = 'basic/habit/habit_delete.html'

class UpdateHabit(UserObjectsMixin,LoginRequiredMixin, UpdateView):
    model = Habit
    success_url = reverse_lazy('habits')
    template_name = 'basic/habit/add_habit.html'
    fields = ['name','goal']

class DeleteTemporalGoal(LoginRequiredMixin,DeleteView):
    model = TemporalGoal
    success_url = reverse_lazy('temporal_goals')
    template_name = 'basic/temporal_goal_htmls/temporal_goal_delete.html'

class UpdateTemporalGoal(UserObjectsMixin,LoginRequiredMixin, UpdateView):
    model = TemporalGoal
    success_url = reverse_lazy('temporal_goals')
    template_name = 'basic/temporal_goal_htmls/add_temporal_goal.html'
    fields = ['name','general_goal','deadline']

class Habits(LoginRequiredMixin, ListView):
    model = Habit
    template_name = 'basic/habit/Habits.html'
    context_object_name = 'habits'
    paginate_by = 3
    login_url = 'users:login'
    def get_queryset(self):
        return HabitService.get_user_habits_with_full_stats(self.request.user)

class HabitStatusUpdateView(UpdateView):
    model = HabitStatus
    form_class = HabitStatusForm
    def form_valid(self, form):
        status = self.get_object()  # Получаем текущий объект из базы, а не из формы
        HabitService.toggle_status(status)
        return redirect('habits')

class TemporalGoals(UserObjectsMixin,LoginRequiredMixin,ListView):
    model = TemporalGoal
    template_name = 'basic/temporal_goal_htmls/temporal_goal.html'
    context_object_name = 'goals'
    login_url = 'users:login'
    paginate_by = 3

class TemporalGoalCheck(LoginRequiredMixin, View):
    def post(self,request,pk):
        goal = get_object_or_404(TemporalGoal,pk = pk, user=request.user)
        GoalService.toggle_goal_completion(goal)
        return redirect('temporal_goals')

class TemporalGoalDetail(LoginRequiredMixin, DetailView,UserObjectsMixin): # вот это God Method
    model = TemporalGoal
    template_name = 'basic/temporal_goal_htmls/temporal_goal_detail.html'
    context_object_name = 'goal'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        general_goal, habits = GoalService.depend_goal(
            temporal_goal=self.object,
            user=self.request.user)
        context['general_goal'] = general_goal
        context['habits'] = habits
        return context

class AddTemporalGoal(LoginRequiredMixin, CreateView):
    model = TemporalGoal
    template_name = 'basic/temporal_goal_htmls/add_temporal_goal.html'
    success_url = reverse_lazy('temporal_goals')
    form_class = AddTgoal
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GeneralGoals(UserObjectsMixin,LoginRequiredMixin,ListView):
    model = GeneralGoal
    template_name = 'basic/general_goal/general_goals.html'
    context_object_name = 'goals'
    login_url = 'users:login'
    paginate_by = 3

class GeneralGoalAdd(LoginRequiredMixin, CreateView):
    model = GeneralGoal
    template_name = 'basic/general_goal/add_general_goal.html'
    form_class = AddGeneralGoal
    success_url = reverse_lazy('general_goals')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class GeneralGoalDelete(LoginRequiredMixin, DeleteView):
    model = GeneralGoal
    template_name = 'basic/general_goal/delete_general_goal.html'
    success_url = reverse_lazy('general_goals')

class GeneralGoalUpdate(LoginRequiredMixin, UpdateView):
    model = GeneralGoal
    template_name = 'basic/general_goal/add_general_goal.html'
    success_url = reverse_lazy('general_goals')
    fields = ['name','description','theme']

class GeneralGoalDetail(LoginRequiredMixin, DetailView,UserObjectsMixin):
    model = GeneralGoal
    template_name = 'basic/general_goal/general_goal.html'
    context_object_name = 'goal'

class GeneralGoalCheck(LoginRequiredMixin, View):
    def post(self, request, pk):
        goal = get_object_or_404(GeneralGoal, pk=pk, user=request.user)
        GoalService.toggle_goal_completion(goal)
        return redirect('general_goals')

def settings(request):
    return render(request, 'basic/core/settings.html')

class CreateTheme(LoginRequiredMixin, CreateView):
    model = Theme
    template_name = 'basic/core/theme.html'
    form_class = CreateTheme
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
