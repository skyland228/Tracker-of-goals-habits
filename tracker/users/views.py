from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView
from .forms import LoginUserForm, RegisterUserForm
from .models import User


class ListUsers(ListView):
    model = User
    template_name = 'users/list.html'
    context_object_name = 'users'

class UserDetail(DetailView):
    model = User
    template_name = 'users/detail_user.html'
    context_object_name = 'user'

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация',}

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:login')