from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label = "Логин")
    password = forms.CharField(widget = forms.PasswordInput(), label = "Пароль")

class RegisterUserForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(), label = "Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(), label = "Повтор пароля")

    class Meta:
        model = get_user_model()
        fields = ['username','email','first_name','last_name','password1','password2']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'E-mail',

        }