from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'auth_users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    #path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    # Add URLs for password reset, etc.
    #path('initial-setup/', views.initial_setup_view, name='initial-setup'),
]