from django.shortcuts import redirect, render, get_object_or_404
from .forms import recipesForm
from django.contrib import messages
from .models import recipesModel

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

#view for search for a recipe
def search_recipe(request):
    model = recipesModel
    
    
    
    
#view for displaying a recipe

#default view for recipe homepage
def recipe_home(request):
    #recipes = recipesModel.objects.all()
    q = request.GET.get("q")
    
    if q:
        recipes = recipesModel.objects.filter(title__icontains=q)
    else:
        recipes = None
    
    
    context = {
        "recipes":recipes
    }
    
    return render(request, 'recipe_home.html',context)