from django import forms
from .models import expenseReport, BudgetCategory
from datetime import datetime, date
from . import helper as h
from .models import ExpenseCategory

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

    #choices for the user. the first item is what the machine sees, the second is what the user sees
    CHOICE = (
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
        (GIVING, 'Giving'),
        (SELF_CARE, 'Self Care'),
        (INVESTING, 'Investing'),
        (MISCELLANEOUS, 'Miscellaneous')
    )
    
    date = forms.DateField(
        widget=forms.DateTimeInput(
            attrs={'class': 'date-time-input', 'placeholder': 'YYYY-MM-DD'},
        ),
        initial=datetime.today().strftime('%Y-%m-%d'),
        label="Date"
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'note-input', 'placeholder': 'Expense Title'}),
        label="Title"
    )

    # Modify the expenseChoices field to use a ModelChoiceField with ExpenseCategory queryset
    expenseChoices = forms.ModelChoiceField(
        widget=forms.Select(attrs={'class': 'your-class-name'}),
        queryset=BudgetCategory.objects.all(),  # Specify the queryset for ExpenseCategory
        label="Expense Category"
    )

    value = forms.DecimalField(
        max_digits=1000,
        widget=forms.NumberInput(attrs={'class': 'value-input'}),
        label="Amount"
    )

    note = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'note-input', 'placeholder': 'Add note'}),
        required=False,
        label="Note"
    )

    class Meta:
        model = expenseReport
        fields = [
            'date', 'title', 'expenseChoices', 'value', 'note'
        ]
        
class DateInput(forms.DateInput):
    input_type = 'date'
    initial = f"{datetime.today().year}-{datetime.today().month}-{datetime.today().day}"

class expenseComparison(forms.Form):
    
    date = forms.DateField(widget=DateInput,initial=f"{datetime.today().year}-{datetime.today().month}-{datetime.today().day}")
    
    toDate = forms.DateField(widget=DateInput,initial=f"{datetime.today().year}-{datetime.today().month}-{datetime.today().day}")
    
    expenseLabelCategory = forms.ChoiceField(choices=[BudgetCategory.objects.all()],label="Category",required=False,initial="INCOME")
    
    checkbox = forms.BooleanField(label='Aggregate', required=False, widget=forms.CheckboxInput)
    
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

class BudgetCategoryForm(forms.ModelForm):
    class Meta:
        model = BudgetCategory
        fields = ['name', 'value'] 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  # Add any additional attributes or classes
            'value': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }