from django.shortcuts import redirect, render, get_object_or_404
from .forms import recipesForm
from django.contrib import messages

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
#view for displaying a recipe