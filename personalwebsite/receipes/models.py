from django.db import models
from django.urls import reverse
from django.utils.timezone import now

class receipesModel(models.Model):
    
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
        return self.name