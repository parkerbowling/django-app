from django import forms
from .models import expenseReport
from datetime import datetime

class expenseReportForm(forms.ModelForm):
    #variable names which the machine sees, redundent but might help me later
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

    #choices for the user. the first item is what the machine sees, the second is what the user sees
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
    
    #the first field the user is able to select
    date = forms.DateField(widget=forms.DateTimeInput(                     #this defaults to today's date to elimate one less button to press
        attrs={'class':'date-time-input','placeholder':'YYYY-MM-DD',}),    #gives it an html class name and placeholder which is redundent
        initial=datetime.today().strftime('%Y-%m-%d'),                     #inital gives the default value (today) and label, well, labels it
        label="Date")
    
    #title of recipe and adds a placeholder in the textbox
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'note-input','placeholder':'Expense Title'}),
        label="Title")
    
    #gives a list of expense choices
    expenseChoices = forms.ChoiceField(widget=forms.Select,                #user is able to select from a list of options
                                       choices=CHOICE,                     #choices are assigned and label for client side
                                       label="Expense Category")
    
    #expense value that user just purchased             
    value = forms.DecimalField(max_digits=1000,                            #gives it the max digits it can take
                               widget=forms.NumberInput(                   #class for HTML and label
                               attrs={'class':'value-input'}),
                               label="Amount")
    #note user can add
    note = forms.CharField(widget=forms.TextInput(attrs={'class':'note-input','placeholder':'Add note'}), #not required but placeholder for what user can add
                                                  required=False,
                                                  label="Note")
    
    #metadata for the report
    class Meta:
        model = expenseReport
        fields = [
            'date','title','expenseChoices','value','note'
        ]