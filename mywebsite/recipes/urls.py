from django.urls import path
from . import views

app_name = 'recipes'
urlpatterns = [
    path('add_recipe/', views.add_recipe, name='add_recipe')
]