# app_name/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User  # Import the User model
from .models import BudgetCategory  # Import your BudgetCategory model

@receiver(post_save, sender=User)
def create_default_budget_category(sender, instance, created, **kwargs):
    """
    Signal handler to create a default budget category for each new user.
    """
    if created:
        # Create a default budget category for the new user
        default_category_name = 'Income'
        BudgetCategory.objects.create(user=instance, name=default_category_name)
