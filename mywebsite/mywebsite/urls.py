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
from expenses.views import *
from auth_users.views import user_login, initial_setup_view

urlpatterns = [
    #name admin path
    path('admin/', admin.site.urls),
    
    #name home path
    #path('home/', home, name="home"),
    
    #path('dashboard/', home, name="dashboard"),
    path('', home, name="home"),
    path('login/',user_login,name='login'),
    path('initial-setup/',initial_setup_view,name='initial-setup'),
    
    # path('dashboard/', home, name="dashbaord"),
    # path('',login,name='login'),
    


    #name expenses urls by including expenses namespace
    path('expenses/',include('expenses.urls',namespace='expenses')),
    path('pie-chart-data/',pie_chart_data,name='pie-chart-data'),
    path('pie-chart-category-data/<str:category>/',pie_chart_category_data,name='pie-chart-category-data'),
    path('expense_home/',expense_home,name="expense_home"),
    path('expense-comparison-barchart/',expense_comparison_barchart,name='expense-comparison-barchart'),
    path('comparison-chart-category-data/<str:category>/<str:date>/',comparison_chart_category_data,name='comparison-chart-category-data'),
    #name expenses urls by including recipes namespace
    path('budget-chart-data/',budget_chart_data,name="budget-chart-data"),
    path('recipes/',include('recipes.urls',namespace='recipes')),
    path('auth_users/', include('auth_users.urls',namespace='auth_users')),
    
    #path('chartGPT/',include('chartGPT.urls',namespace='chartGPT')),
    
    #path("auth_users/",include('auth_users.urls')),
    #path("auth_users/",include('django.contrib.auth.urls'))
    
]
