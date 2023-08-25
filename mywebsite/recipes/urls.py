from django.urls import path
from . import views
from .views import RecipeListView, RecipeAddView

#declares app name for namespace
app_name = 'recipes'
urlpatterns = [
    #path('add_recipe/', views.add_recipe, name='add_recipe'),
    #path('recipe_home/',views.recipe_home,name='recipe_home')
    path('recipe_home/',RecipeListView.as_view(),name='recipe_home'),
    path('add_recipe/',RecipeAddView.as_view(),name='add_recipe')
    
]