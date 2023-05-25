from django import forms
from .models import expenseReport
import datetime

class expenseReportForm(forms.ModelForm):
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
        (HEALTHCARE, 'Healthcare')    
    )
    date = forms.DateField(widget=forms.DateTimeInput(attrs={
        'class':'date-time-input','placeholder':'YYYY-MM-DD'
        }))
    expenseChoices = forms.MultipleChoiceField(widget=forms.Select(choices=EXPENSE_CHOICES,attrs={
        'class':'expense-choices'
    }))
    note = forms.CharField(widget=forms.TextInput(attrs={
        'class':'note-input','placeholder':'Add note'
        }))
    value = forms.DecimalField(max_digits=1000,widget=forms.NumberInput(attrs={
        'class':'value-input'
    }))
    
    class Meta:
        model = expenseReport
        fields = [
            'date','expenseChoices','value','note'
        ]