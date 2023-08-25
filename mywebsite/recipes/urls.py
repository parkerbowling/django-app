from django.urls import path
from . import views

#declares app name for namespace
app_name = 'recipes'
urlpatterns = [
    path('add_recipe/', views.add_recipe, name='add_recipe'),
    path('recipe_home/',views.recipe_home,name="recipe_home")
]