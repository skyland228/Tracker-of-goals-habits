from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from goals.service.general_service import StatsService
from .forms import RegisterUserForm

class LoginUser(LoginView):
    form_class = AuthenticationForm # я использую кастомные формы только для замены меток для полей зачем
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация',}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

class Profile(TemplateView):
    template_name = 'core/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stats = StatsService.calculate_stats(self.request.user)
        context.update({
            'user': self.request.user,
            'today_progress': stats['today_progress'],
            'total_progress': stats['total_progress'],
            'streak': stats['streak']})
        return context