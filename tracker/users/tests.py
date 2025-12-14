from django.test import TestCase
from .forms import RegisterUserForm

class AuthorizationTest(TestCase):
  #мы создаем не корректные данные для создания формы
  data = {
  "username": "testuserРу", # Тут русские символы
  "password1": "strongpass123!", # тут нет англ заглавной буквы
  "password2": "strongpass123!"} 
  def test_register_with_incorrect_name(self):
    '''Тестирование регистрации пользователя с именем содержащие ру символы'''
    form = RegisterUserForm(self.data)
    self.assertIn('No', form.errors['username'][0]) # делаю мягкую проверку ошибка "No Ru symbols"
  def test_password(self):
    '''Тестирование регистрации пользователя с паролем без заглавной буквы'''
    form = RegisterUserForm(self.data)
    self.assertFormError(form, 'password2', 'password must to contain a capital letter') # тут полная проверка

def test_profile():
  pass