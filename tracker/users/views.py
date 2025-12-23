from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.forms import AuthenticationForm
from users.services.general_service import StatsService
from .forms import RegisterUserForm
from .models import Profile

class LoginUser(LoginView):
    form_class = AuthenticationForm 
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация',}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

class ProfileUser(TemplateView):
    template_name = 'users/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)  # или get_object_or_404
        context.update({
            'profile': profile,
            'user': self.request.user})
        return context
    
class Statistics(TemplateView):
    template_name = 'users/statistics.html'
    def get_context_data(self, **kwargs):
        stats = StatsService.calculate_stats(self.request.user)
        context = super().get_context_data(**kwargs)   
        context.update({'stats':stats})  
        return context 