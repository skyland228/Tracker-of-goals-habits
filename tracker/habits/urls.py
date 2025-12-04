from django.urls import path
from . import views
app_name = 'habits' 

urlpatterns = [
  path('', views.Habits.as_view(), name='habits'),
  path('add/',views.AddHabit.as_view(), name='add_habit'),
  path('status/<int:pk>/update/',views.HabitStatusUpdate.as_view(), name = 'habit_status_update'),
  path('delete/<int:pk>/', views.DeleteHabit.as_view(), name='delete_habit'),
  path('update/<int:pk>/', views.UpdateHabit.as_view(), name='update_habit'),
]