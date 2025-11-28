from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Habit

class Habits(LoginRequiredMixin, ListView):
  model = Habit
  template_name = 'habits/Habits.html'
  context_object_name = 'habits'
  login_url = 'users:login'
  def get_queryset(self):
    pass