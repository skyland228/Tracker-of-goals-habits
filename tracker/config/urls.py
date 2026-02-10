from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
    path('habits/', include('habits.urls', namespace='habits')),
    path('goals/', include('goals.urls')),
    path('users/', include('users.urls', namespace="users")),
    path('appearance/', include('appearance.urls')),
    path('api/v1/', include('goals.api.urls')),
    path('api/v1/', include('habits.api.urls')),
    path('api/v1/', include('users.api.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)