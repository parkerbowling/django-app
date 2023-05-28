from django.urls import path
from . import views

app_name = 'expenses'
urlpatterns = [
    path('add_expense/', views.add_expense, name='add_expense')
]