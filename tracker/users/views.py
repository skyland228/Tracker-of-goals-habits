from django.contrib.auth.views import LoginView 
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from users.services.general_service import StatsService
from .forms import RegisterUserForm, ChangeProfileForm
from django.contrib.auth import get_user_model
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

class ProfileUser(LoginRequiredMixin, UpdateView):
    form_class = ChangeProfileForm
    template_name = 'users/profile.html'
    model = get_user_model()
    success_url = reverse_lazy('users:profile')
    def get_object(self):
        return self.request.user

class Statistics(TemplateView):
    template_name = 'users/statistics.html'
    def get_context_data(self, **kwargs):
        stats = StatsService.calculate_stats(self.request.user)
        context = super().get_context_data(**kwargs)   
        context.update({'stats':stats})  
        return context 