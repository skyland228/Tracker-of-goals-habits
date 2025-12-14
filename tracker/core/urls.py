from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('theme/create/', views.CreateTheme.as_view(), name='theme_create'),
    path('users/', include('users.urls', namespace="users")),
    path('habits/', include('habits.urls', namespace='habits')),
    path('', include('goals.urls')),
]
