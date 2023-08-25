from django.shortcuts import redirect, render
from .forms import recipesForm
from django.contrib import messages
from .models import recipesModel
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DetailView,
    DeleteView
)

#have one view for adding a recipe
def add_recipe(request):
    form = recipesForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            print("do we get here")
            form.save()
            messages.success(request,"Recipe Added!")
            return redirect('recipes:add_recipe')
        
    context = {
        "form":form
    }
    return render(request, 'add_recipe.html',context)

def redirect_to_add_recipe(request):
    return redirect('add_recipe')

#view for search for a recipe
def search_recipe(request):
    model = recipesModel
    
    
    
    
#view for displaying a recipe

#default view for recipe homepage
#will want to add trigram similarity eventually, django package <-
def recipe_home(request):
    #get query
    q = request.GET.get("q")
    
    if q:
        vector = SearchVector('title')
        query = SearchQuery(q)
        recipes = recipesModel.objects.annotate(rank=SearchRank(vector,query)).filter(rank__gte=0.001).order_by('-rank')
    
    else:
        recipes = recipesModel.objects.all()
        
    add_recipe_button_click = request.GET.get("add-new-recipe")    
    print('eheree')
    
    context = {
        "recipes":recipes
    }
    
    return render(request, 'recipe_home.html',context)