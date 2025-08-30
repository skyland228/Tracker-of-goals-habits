from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('add_habit/',views.AddHabits.as_view(), name = 'add_habit'),
    path('profile/',views.Profile.as_view(), name = 'profile'),
    path('habits/', views.Habits.as_view(), name = 'habits'),
    path('status/<int:pk>/update/', views.HabitStatusUpdateView.as_view(), name='habitstatus_update'),
    path('general_goals/', views.GeneralGoals.as_view(), name = 'general_goals'),
    path('temporal_goals/', views.TemporalGoals.as_view(), name='temporal_goals'),
]
