from django.db import models
from django.urls import reverse
from django.utils.timezone import now

# Create your models here.
class expenseReport(models.Model):    
    RENT_MORTAGAGE = 'RENT_MORTGAGE'
    GAS_REPAIRS = 'GAS_REPAIRS'
    INCOME = 'INCOME'
    TAXES = 'TAXES'
    UTILITIES = 'UTILITIES'
    GROCERIES = 'GROCERIES'
    DINE_OUT = 'DINE_OUT'
    ENTERTAINMENT = 'ENTERTAINMENT'
    TRAVEL = 'TRAVEL'
    SHOPPING = 'SHOPPING'
    HOME_IMPROVEMENT = 'HOME_IMPROVEMENT'
    HEALTHCARE = 'HEALTHCARE'
    GIVING = 'GIVING'

    EXPENSE_CHOICES = (
        (RENT_MORTAGAGE,'Rent/Mortgage'),
        (GAS_REPAIRS, 'Gas/Vehicle Repairs'),
        (INCOME, 'Income'),
        (TAXES, 'Taxes'),
        (UTILITIES, 'Utilites'),
        (GROCERIES, 'Groceries'),
        (DINE_OUT, 'Dine Out'),
        (ENTERTAINMENT, 'Entertainment'),
        (TRAVEL, 'Travel'),
        (SHOPPING, 'Shopping'),
        (HOME_IMPROVEMENT, 'Home Improvement and Repairs'),
        (HEALTHCARE, 'Healthcare'),    
        (GIVING,'Giving')
    )
    
    date = models.DateField(default=now)
    expenseChoices = models.TextField(choices=EXPENSE_CHOICES)
    value = models.DecimalField(decimal_places=2,max_digits=1000)
    note = models.TextField(max_length=140)

    def __str__(self):
        return self.name
