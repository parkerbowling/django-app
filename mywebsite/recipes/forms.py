from django import forms
from .models import recipesModel
from datetime import datetime
from django.urls import reverse

class recipesForm(forms.ModelForm):
    #make meal choices
    MEALCHOICE = (
    ("BREAKFAST","Breakfast"),
    ("LUNCH","Lunch"),
    ("DINNER","Dinner"),
    ("DESSERT","Dessert"),
    ("APPETIZER","Appetizer")
    )
    
    #date added with inital default date, and label for Date
    date = forms.DateField(widget=forms.DateTimeInput(
        attrs={'class':'date-time-input','placeholder':'YYYY-MM-DD',}),
        initial=datetime.today().strftime('%Y-%m-%d'),
        label="Date")
    
    #title of recipe and adds a placeholder in the textbox
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'note-input','placeholder':'Recipe Title'}),
        label="Title")
    
    #choose meal type with Select widget
    meal_type = forms.ChoiceField(widget=forms.Select,choices=MEALCHOICE,label="Meal Type")
    
    #list ingredients in comma separated values and add label
    ingredients = forms.CharField(widget=forms.Textarea(attrs={'class':'note-input','placeholder':'Add add each ingredient on a new line.','rows':1,'cols':45}),
                                                        label="Ingredients")
    
    #add instructions to be used later as well
    instructions = forms.CharField(widget=forms.TextInput(attrs={'class':'note-input','placeholder':'Add instructions'}),
                                                        label="Instructions")
    
    #metadata class for fields for form
    class Meta:
        model = recipesModel
        fields = ['date','title','meal_type','ingredients','instructions']
        
    def get_absolute_url(self):
        return reverse("recipes:recipe_detail", kwargs={"id": self.id})
    