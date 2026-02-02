import re
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from users.models import Profile

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
    image = forms.ImageField(required=False, label="Фото")
    first_name = forms.CharField(label="Имя")
    last_name = forms.CharField(label="Фамилия")
    email = forms.EmailField(label="Email")
    bio = forms.CharField(label="Биография", widget=forms.Textarea)
    class Meta:
        model = get_user_model()
        fields = ['image','first_name', 'last_name',  'bio','email']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if self.instance and hasattr(self.instance, 'profile'):
            profile = self.instance.profile
            self.fields['image'].initial = profile.image
            self.fields['bio'].initial = profile.bio
def save(self, commit = True):
    user = super().save()
    if user.pk:
        profile, created = Profile.objects.get_or_create(user=user)
        if self.cleaned_data.get('image'):
            if profile.image:
                profile.image.delete(save=False)
            profile.image = self.cleaned_data['image']

        profile.bio = self.cleaned_data.get('bio', '')
        if commit:
            profile.save()
    return user