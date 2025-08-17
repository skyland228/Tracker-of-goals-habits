from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('profile/',views.profile, name = 'profile'),
    path('habits/', views.habits, name = 'habits'),
    path('goals/', views.goals, name = 'goals'),
    path('progress/', views.progress, name = 'progress'),
]
