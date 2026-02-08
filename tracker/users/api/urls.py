from rest_framework import routers
from . import views
from django.urls import path, include

router = routers.SimpleRouter()
router.register(r'users',views.UserApiView)

urlpatterns = [
  path("", include(router.urls)),                 
  path("telegram/connect/", views.TelegramConnectView.as_view()),  
]