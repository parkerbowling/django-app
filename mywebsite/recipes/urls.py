from django.urls import path
from .views import RecipeListView, RecipeAddView, RecipeDetailView, RecipeUpdateView

#declares app name for namespace
app_name = 'recipes'
urlpatterns = [
    path('recipe_home/',RecipeListView.as_view(),name='recipe_home'),
    path('add_recipe/',RecipeAddView.as_view(),name='add_recipe'),
    path('<int:id>/',RecipeDetailView.as_view(),name='recipe_detail'),
    path('<int:id>/update',RecipeUpdateView.as_view(),name='recipe_update')
    
]