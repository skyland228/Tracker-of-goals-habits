import re
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError


class RegisterUserForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(), label = "Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput(), label = "Повтор пароля")

    class Meta:
        model = get_user_model()
        fields = ['username','email','password1','password2']
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'E-mail',
        }
    def clean_username(self):
        username = self.cleaned_data['username']
        if re.search('[а-яА-Я]', username):
            raise ValidationError('No Ru symbols')
        return username
    def clean_password2(self):
        password = self.cleaned_data['password2']
        if not (re.search('[A-Z]', password)):
            raise ValidationError('password must to contain a capital letter')
        return password

class ChangeProfileForm(forms.ModelForm):
    image = forms.ImageField(required = False)
    bio   = forms.CharField (required = False, widget = forms.Textarea)
    class Meta:
        model = get_user_model()
        fields = ['first_name','last_name','image','email','bio']
