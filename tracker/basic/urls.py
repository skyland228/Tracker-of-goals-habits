from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('profile/', views.Profile.as_view(), name='profile'),
    # {% block 'habits' %}
    path('habits/', views.Habits.as_view(), name='habits'),
    path('habits/<int:pk>/update', views.UpdateHabit.as_view(), name='update_habit'),
    path('add_habit/',views.AddHabits.as_view(), name = 'add_habit'),
    path('habits/<int:pk>/delete/',views.DeleteHabit.as_view(), name='delete_habit'),
    path('status/<int:pk>/update/', views.HabitStatusUpdateView.as_view(), name='habitstatus_update'),
    # {% endblock %}
    # {% block 'temporal_goals' %}
    path('temporal_goals/', views.TemporalGoals.as_view(), name='temporal_goals'),
    path('temp_status/<int:pk>/update/', views.TemporalGoalCheck.as_view(), name='temporal_update'),
    path('temporal_goals/<int:pk>/update/', views.UpdateTemporalGoal.as_view(), name='update_temporal_goal'),
    path('temporal-goal/<int:pk>/', views.TemporalGoalDetail.as_view(), name='temporal_goal_detail'),
    path('temporal_goals/add/', views.AddTemporalGoal.as_view(), name='temporal_goal_add'),
    path('temporal-goal/<int:pk>/delete/', views.DeleteTemporalGoal.as_view(), name='delete_temporal_goal'),
    # {% endblock %}
    path('general_goals/', views.GeneralGoals.as_view(), name = 'general_goals'),
]
