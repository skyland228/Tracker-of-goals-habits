from django.urls import path
from . import views
app_name = 'habits' 

urlpatterns = [
  path('list/', views.Habits.as_view(), name='habits'),
]