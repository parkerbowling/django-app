from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .forms import recipesForm
from .models import recipesModel

from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView
)

class RecipeListView(ListView):
    template_name = "recipe_home.html"
    queryset = recipesModel.objects.all()
    context_object_name = 'filtered_results'
    
    def get_queryset(self):
        result = None

        text_query = self.request.GET.get('text-filter')
        category_query = self.request.GET.get('category-filter')
        
        if text_query == None:
            return recipesModel.objects.all()  
        
        if text_query != '' or category_query != "None":
        
            if text_query == "" and category_query == "None":
                return result
            elif text_query != "" and category_query == "None":
                postresult = recipesModel.objects.filter(title__icontains=text_query)
                result = postresult
            elif text_query == "" and category_query != "None":
                print("here")
                postresult = recipesModel.objects.filter(meal_type__iexact=category_query)
                result=postresult
            elif text_query != "" and category_query != "None":
                postresult = recipesModel.objects.filter(title__icontains=text_query, meal_type__iexact=category_query)
                result=postresult
        else:
            result = recipesModel.objects.all()    
    
        return result
    
class RecipeDetailView(DetailView):
    template_name = "recipe_detail.html"
    queryset = recipesModel.objects.all()
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(recipesModel,id=id_)
            
class RecipeAddView(CreateView):
    template_name = "add_recipe.html"
    queryset = recipesModel.objects.all()
    form_class = recipesForm
    
    def form_valid(self, form):
        print(form.cleaned_data) 
        return super().form_valid(form)
    
#success_url does not work, not sure why but can fix later
class RecipeUpdateView(UpdateView):
    template_name = "update_recipe.html"
    form_class = recipesForm
    success_url = "/recipes/recipe_detail"
    
    def form_valid(self, form):
        print(form.cleaned_data)
        #redirect_url = super(RecipeUpdateView, self).form_valid(form)
        return super().form_valid(form)
    
    def get_object(self):
        id_ = self.kwargs.get("id")
        return get_object_or_404(recipesModel,id=id_)
    
    def get_success_url(self):
        return reverse('recipes:recipe_detail',kwargs={'id': self.object.id })