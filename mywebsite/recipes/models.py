from django.db import models
from django.urls import reverse
from django.utils.timezone import now

#see forms.py
class recipesModel(models.Model):
    
    MEALCHOICE = (
        ("BREAKFAST","Breakfast"),
        ("LUNCH","Lunch"),
        ("DINNER","Dinner"),
        ("DESSERT","Dessert"),
        ("APPETIZER","Appetizer")
    )
    
    date = models.DateField(default=now)
    title = models.CharField(max_length=128)
    meal_type = models.TextField(choices=MEALCHOICE)
    ingredients = models.CharField(max_length=2000)
    instructions = models.CharField(max_length=2000)
    
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("recipes:recipe_detail", kwargs={"id": self.id})
    
