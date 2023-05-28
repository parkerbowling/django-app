from django.urls import path
from . import views

app_name = 'receipes'
urlpatterns = [
    path('add_receipe/', views.add_receipe, name='add_receipe')
]