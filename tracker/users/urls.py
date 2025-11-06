from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('login/', views.LoginUser.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name = 'logout'),
    path('register/', views.RegisterUser.as_view(), name = 'register'),
    path('list_users/', views.ListUsers.as_view(), name = 'list_users'),
    path('detail_user/<int:pk>/', views.UserDetail.as_view(), name = 'detail_user'),
]
