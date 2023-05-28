from django.urls import path
from . import views

#defines the app name for a namespace to be used in personalwebsite/urls.py
app_name = 'expenses'

#the url pattern that links expenses/add_expense to personalwebsite/urls.py
urlpatterns = [
    path('add_expense/', views.add_expense, name='add_expense')
]