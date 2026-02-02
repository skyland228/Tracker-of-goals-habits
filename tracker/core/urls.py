from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from core import settings
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('theme/create/', views.CreateTheme.as_view(), name='theme_create'),
    path('users/', include('users.urls', namespace="users")),
    path('habits/', include('habits.urls', namespace='habits')),
    path('', include('goals.urls')),
    path('api/v1/', include('goals.api.urls')),
    path('api/v1/', include('habits.api.urls')),
    path('api/v1/', include('users.api.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)