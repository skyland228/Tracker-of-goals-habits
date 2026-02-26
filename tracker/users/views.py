from django.contrib.auth.views import LoginView 
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .models import TelegramLinkToken
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from users.services.general_service import StatsService
from .forms import RegisterUserForm, ChangeProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginUser(LoginView):
    form_class = AuthenticationForm 
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация',}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')

class Statistics(LoginRequiredMixin,TemplateView):
    template_name = 'users/statistics.html'
    login_url = 'users:login'
    def get_context_data(self, **kwargs):
        stats = StatsService.calculate_stats(self.request.user)
        context = super().get_context_data(**kwargs)   
        context.update({'stats':stats})  
        return context 
    
class Profile(UpdateView):
    form_class = ChangeProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset = None):
        return self.request.user
    
@login_required
def connect_telegram(request):
    token_obj = TelegramLinkToken.create_token(request.user)
    link = f'https://t.me/skylandbot_bot?start={token_obj.token}'
    return redirect(link)
