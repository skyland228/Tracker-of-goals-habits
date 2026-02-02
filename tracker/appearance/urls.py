from django.urls import path
from . import views

urlpatterns = [
  path('theme/create/', views.CreateTheme.as_view(), name='create_theme'),
]

    