from django import forms
from .models import receipesModel
from datetime import datetime

class receipesForm(forms.ModelForm):
    MEALCHOICE = (
    ("BREAKFAST","Breakfast"),
    ("LUNCH","Lunch"),
    ("DINNER","Dinner"),
    ("DESSERT","Dessert"),
    ("APPETIZER","Appetizer")
    )
    
    date = forms.DateField(widget=forms.DateTimeInput(
        attrs={'class':'date-time-input','placeholder':'YYYY-MM-DD',}),
        initial=datetime.today().strftime('%Y-%m-%d'),
        label="Date")
    
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'note-input','placeholder':'Receipe Name'}),
        label="Title")
    
    meal_type = forms.ChoiceField(widget=forms.Select,choices=MEALCHOICE,label="Meal Type")
    
    ingredients = forms.CharField(widget=forms.Textarea(attrs={'class':'note-input','placeholder':'Add commna separated ingredients','rows':1,'cols':33}),
                                                        label="Ingredients")
    instructions = forms.CharField(widget=forms.TextInput(attrs={'class':'note-input','placeholder':'Add instructions'}),
                                                        label="Instructions")
    
    class Meta:
        model = receipesModel
        fields = ['date','title','meal_type','ingredients','instructions']
    