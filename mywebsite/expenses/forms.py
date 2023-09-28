from django import forms
from .models import expenseReport
from datetime import datetime, date
from . import helper as h

class DateSelectorWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        days = [(day, day) for day in [1]]
        months = [(month, month) for month in range(1, 13)]
        years = [(year, year) for year in range(2022, (datetime.today().year)+10)]
        widgets = [
            #forms.Select(attrs=attrs,choices=days),
            forms.HiddenInput(attrs=attrs),
            forms.Select(attrs=attrs, choices=months),
            forms.Select(attrs=attrs, choices=years),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if isinstance(value, date):
            return [value.day, value.month, value.year]
        elif isinstance(value, str):
            year, month, day = value.split("-")
            return [day, month, year]
        return [None, None, None]

    def value_from_datadict(self, data, files, name):
        day, month, year = super().value_from_datadict(data, files, name)
        # DateField expects a single string that it can parse into a date.
        return "{}-{}-{}".format(year, month, day)

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
        
#what is going on here? need to create dropdown selector??
#        
#   [Category] -- From [Month/Year] to [Month/Year] by [Month/Year]
#
#
class DateInput(forms.DateInput):
    input_type = 'date'
    initial = f"{datetime.today().year}-{datetime.today().month}-{datetime.today().day}"

class expenseComparison(forms.Form):
      
    #GET RID OF REQUIRED SOMETHING IS WRONG
    # date = forms.DateField(widget=DateSelectorWidget(),label="From:")
    # #attrs={'onchange': 'expenseComparison.submit();'}
    # toDate = forms.DateField(widget=DateSelectorWidget(),label="To:",initial=datetime.today())
    
    date = forms.DateField(widget=DateInput,initial=f"{datetime.today().year}-{datetime.today().month}-{datetime.today().day}")
    
    toDate = forms.DateField(widget=DateInput,initial=f"{datetime.today().year}-{datetime.today().month}-{datetime.today().day}")
    
    expenseLabelCategory = forms.ChoiceField(choices=[(x,x) for x in h.getExpenseCategories("all")],label="Category",required=False,initial="INCOME")
    
    def getFromMonth(self):
        return self.date.month
    
    def getFromYear(self):
        return self.date.year
    
    def getToMonth(self):
        return self.toDate.month
    
    def getToYear(self):
        return self.toDate.year
    
    def clean(self):
        cleaned_data = super(expenseComparison, self).clean()
        from_time = cleaned_data.get("date")
        end_time = cleaned_data.get("toDate")

        if from_time and end_time:
            if end_time < from_time:
                raise forms.ValidationError("End date cannot be earlier than start date!")
        return cleaned_data
    
    