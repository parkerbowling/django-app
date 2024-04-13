from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.contrib.auth.models import User

#see forms.py
class recipesModel(models.Model):
    
    MEALCHOICE = (
        ("BREAKFAST","Breakfast"),
        ("LUNCH","Lunch"),
        ("DINNER","Dinner"),
        ("DESSERT","Dessert"),
        ("APPETIZER","Appetizer")
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')  # Link expense to a user
    date = models.DateField(default=now)
    title = models.CharField(max_length=128)
    meal_type = models.TextField(choices=MEALCHOICE)
    ingredients = models.CharField(max_length=2000)
    instructions = models.CharField(max_length=2000)
    
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("recipes:recipe_detail", kwargs={"id": self.id})
    
