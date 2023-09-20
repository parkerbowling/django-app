from django.shortcuts import redirect, render
from django.db.models import Count, Q, Sum
from .models import expenseReport
from .forms import expenseReportForm
from django.contrib import messages
from django.http import JsonResponse

#temporary home page for now
def home(request):
    #render takes in a request and an HTML page to render to view
    return render(request, 'home.html')

def expense_home(request):
    
    return render(request,'expense_home.html')

#add_expense is the page where user can add expense
def add_expense(request):

    #define a form to be used. Arguments POST it to the view if a POST is requested or post an empty form
    form = expenseReportForm(request.POST or None)

    #if the method is a POST, save form and return success and redirect to a new form
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense added!')
            return redirect('expenses:add_expense')
        
    #context allows variables to be passed into the HTML file, see HTML file named below
    context = {
        "form":form
    }
    return render(request, 'add_expense.html', context)

def chart_data(request):
    
    #dynamically get the Categories in case I decide to add or remove one of them and make them unique
    setCategories = expenseReport.objects.values("expenseChoices")
    newSet = list(set([i[1] for s in [d.items() for d in setCategories] for i in s]))
    
    #name a json structure for inserting data into chart
    allCategoryData = {
        "name": "Expenses",
        "data": []
    }
    
    #for every category (remember not all categories may have appeared yet) sum the values and add to data
    #will need to be able to filter on certain dates, like months and years
    for i in newSet:
        
        #gets all values for category and sums
        categorySum = expenseReport.objects.values("value").filter(expenseChoices=str(i)).aggregate(Sum('value'))['value__sum']

        data = {
            'name':str(i),
            'y': float(categorySum)
        }
        allCategoryData['data'].append(data)
    
    #need to include updating for month and year selection
    
    #json chart configuration
    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Total Expenses'},
        'tooltip': {
            'format': 
                '{series.name}: <b>${y}</b><br/>',
                'shared':'true'
        },
        'series': [allCategoryData]
    }
    
    #return a JsonResponse so Highchart knows what to do with our data
    return JsonResponse(chart)
