from django.db import models
from django.utils.timezone import now

#See forms.py for more details
class expenseReport(models.Model):    
    RENT_MORTAGAGE = 'RENT_MORTGAGE'
    GAS_TRANSIT = 'GAS_TRANSIT'
    INCOME = 'INCOME'
    TAXES = 'TAXES'
    UTILITIES = 'UTILITIES'
    GROCERIES = 'GROCERIES'
    DINE_OUT = 'DINE_OUT'
    ENTERTAINMENT = 'ENTERTAINMENT'
    TRAVEL = 'TRAVEL'
    SHOPPING = 'SHOPPING'
    REPAIRS = 'REPAIRS'
    HEALTHCARE = 'HEALTHCARE'
    GIVING = 'GIVING'
    SELF_CARE = 'SELF_CARE'
    INVESTING = 'INVESTING'
    MISCELLANEOUS = 'MISCELLANEOUS'

    EXPENSE_CHOICES = (
        (RENT_MORTAGAGE,'Rent/Mortgage'),
        (GAS_TRANSIT, 'Gas/Transit'),
        (INCOME, 'Income'),
        (TAXES, 'Taxes'),
        (UTILITIES, 'Utilites'),
        (GROCERIES, 'Groceries'),
        (DINE_OUT, 'Dine Out'),
        (ENTERTAINMENT, 'Entertainment'),
        (TRAVEL, 'Travel'),
        (SHOPPING, 'Shopping'),
        (REPAIRS, 'Repairs'),
        (HEALTHCARE, 'Healthcare'),    
        (GIVING,'Giving'),
        (SELF_CARE,'Self Care'),
        (INVESTING,'Investing'),
        (MISCELLANEOUS, 'Miscellaneous')
    )
    
    #see forms for more details
    date = models.DateField(default=now)
    title = models.CharField(max_length=128)
    expenseChoices = models.TextField(choices=EXPENSE_CHOICES)
    value = models.DecimalField(decimal_places=2,max_digits=1000)
    note = models.TextField(max_length=140)

    def __str__(self):
        return self.title
