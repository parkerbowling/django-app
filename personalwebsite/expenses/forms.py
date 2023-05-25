from django import forms
from .models import expenseReport
from datetime import datetime

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
    GIVING = 'GIVING'

    CHOICE = (
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
        (GIVING, 'Giving')
    )
    date = forms.DateField(widget=forms.DateTimeInput(
        attrs={'class':'date-time-input','placeholder':'YYYY-MM-DD',}),
        initial=datetime.today().strftime('%Y-%m-%d'),
        label="Date")
    
    expenseChoices = forms.ChoiceField(widget=forms.Select,
                                       choices=CHOICE,
                                       label="Expense Category")
    value = forms.DecimalField(max_digits=1000,
                               widget=forms.NumberInput(
                               attrs={'class':'value-input'}),
                               label="Amount")
    note = forms.CharField(widget=forms.TextInput(attrs={'class':'note-input','placeholder':'Add note'}),
                                                  required=False,
                                                  label="Note")
    
    class Meta:
        model = expenseReport
        fields = [
            'date','expenseChoices','value','note'
        ]