from django.contrib import admin
from django.urls import path, include

from .views import Main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls', namespace="users")),
    path('', include('basic.urls')),
    path('', Main, name = 'home')
]
