"""
URL configuration for mywebsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# importing from app folder, the view file
from expenses.views import home
from auth_users.views import login_user

urlpatterns = [
    #name admin path
    path('admin/', admin.site.urls),
    
    #name home path
    #path('home/', home, name="home"),
    
    path('', home, name="home"),
    
    #name a login path
    #path('auth_users/',include('auth_users.urls')),

    #name expenses urls by including expenses namespace
    path('expenses/',include('expenses.urls',namespace='expenses')),
    
    #name expenses urls by including recipes namespace
    path('recipes/',include('recipes.urls',namespace='recipes')),
    
    #path("auth_users/",include('auth_users.urls')),
    #path("auth_users/",include('django.contrib.auth.urls'))
    
]
