from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView,UpdateView,DeleteView, CreateView
from .models import Habit, HabitStatus
from .services.habit_service import HabitServices
from django.urls import reverse_lazy
from .forms import AddHabit, HabitStatusForm

class Habits(LoginRequiredMixin, ListView):
  model = Habit
  template_name = 'habits/habits.html'
  context_object_name = 'habits'
  login_url = 'users:login'

  def get_queryset(self):
    return HabitServices.get_user_habit_stats(self.request.user) # создаем статусы для вывода привычек
  
class AddHabit(LoginRequiredMixin, CreateView):
  model = Habit
  form_class = AddHabit
  template_name = 'habits/habit_add.html'
  success_url = reverse_lazy('habits:habits')

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

  def form_valid(self, form):
    form.instance.user = self.request.user # назначаем пользователя для привычки
    return super().form_valid(form) # сохранили нашу привычку и редирект
  
class DeleteHabit(LoginRequiredMixin, DeleteView):
  model = Habit
  template_name = 'habits/habit_delete.html'
  success_url = reverse_lazy('habits:habits')

class UpdateHabit(LoginRequiredMixin, UpdateView):
  model = Habit
  template_name = 'habits/habit_add.html'
  fields = ['name', 'goal']
  success_url = reverse_lazy('habits:habits')

class HabitStatusUpdate(LoginRequiredMixin, UpdateView):
  model = HabitStatus
  form_class = HabitStatusForm

  def form_valid(self,form):
    status = self.get_object()
    HabitServices.change_status(status) # делаем смену статуса
    return redirect('habits:habits')