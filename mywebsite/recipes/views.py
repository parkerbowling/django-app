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
    context_object_name = 'all_search_results'
    
    def get_queryset(self):
       result = super(RecipeListView, self).get_queryset()
       query = self.request.GET.get('q')
       if query:
          postresult = recipesModel.objects.filter(title__icontains=query)
          result = postresult
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