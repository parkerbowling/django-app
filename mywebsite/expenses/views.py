from django.shortcuts import redirect, render
from django.db.models import Count, Q, Sum
from .models import expenseReport
from .forms import expenseReportForm
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime

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
    newSet.remove("INCOME")
    #name a json structure for inserting data into chart
    allCategoryData = {
        "name": "Expenses",
        "data": []
    }
    
    #for every category (remember not all categories may have appeared yet) sum the values and add to data
    #will need to be able to filter on certain dates, like months and years
    dateNow = datetime.now()
    currentYear = dateNow.year
    currentMonth = dateNow.month
    print(currentYear)
    print(currentMonth)
    
    for i in newSet:
        
        #gets all values for category and sums
        if True:
            categorySum = expenseReport.objects.values("value"
                    ).filter(
                        date__year=currentYear, date__month=currentMonth
                    ).filter(
                        expenseChoices=str(i)).aggregate(
                    Sum('value'))['value__sum']
                        
        # will need an else statement if user wants to see lifetime expenses (all)
        # else:
        #
        #     categorySum = expenseReport.objects.values("value"
        #             ).filter(
        #                 expenseChoices=str(i)).aggregate(
        #             Sum('value'))['value__sum']
            
        #if there is no data, no need to add to chart     
        if categorySum == None:
            continue

        data = {
            'name':str(i),
            'y': float(categorySum)
        }
        allCategoryData['data'].append(data)
        
    #depending on selection, change this
    chartTitle = ""
    if True:
        chartTitle = f"Total Expenses This Month {currentMonth}/{currentYear}"
    # else:
    #     chartTitle = "Total Expenses All"
        
    #json chart configuration
    chart = {
        'chart': {'type': 'pie', 'renderTo':'expenses-pie-container'},
        'title': {'text': chartTitle},
        'tooltip': {
            'format': 
                '{series.name}: <b>${y}</b><br/>',
                'shared':'true'
        },
        'series': [allCategoryData]
    }
    
    #return a JsonResponse so Highchart knows what to do with our data
    return JsonResponse(chart)

def sankey_chart(request):
    
    #get category names, should these be helper functions?
    setCategories = expenseReport.objects.values("expenseChoices")
    newSet = list(set([i[1] for s in [d.items() for d in setCategories] for i in s]))
    newSet.remove("INCOME")
    
    data = []
    
    #get current dates
    dateNow = datetime.now()
    currentYear = dateNow.year
    currentMonth = dateNow.month
    
    #get the income total
    incomeSum = expenseReport.objects.values("value"
                    ).filter(
                        date__year=currentYear, date__month=currentMonth
                    ).filter(
                        expenseChoices=str("INCOME")).aggregate(
                    Sum('value'))['value__sum']
              
    #check for no income          
    if incomeSum == None:
        incomeSum = 0
               
    #get all expenses  
    expensesSum = 0  
    expensesDict = {}
                       
    for i in newSet:
        categorySum = expenseReport.objects.values("value"
                    ).filter(
                        date__year=currentYear, date__month=currentMonth
                    ).filter(
                        expenseChoices=str(i)).aggregate(
                    Sum('value'))['value__sum']
        if categorySum == None:
            continue
        
        expensesDict[i] = float(categorySum)
        
        expensesSum += float(categorySum)
        
    #calculate income and savings
    incomeSum = float(incomeSum)
    savingsSum = incomeSum - expensesSum
        
    #append for json file                
    data.append(
        ['Income','Savings',savingsSum]
    )
    data.append(
        ['Income','Expenses',expensesSum]
    )

    for index, key in expensesDict.items():
        data.append(
            ['Expenses',index,key]
        )

    #add if else when chart wants to be changed
    chartTitle = ""
    if True:
        chartTitle = f"Expense and Savings This Month {currentMonth}/{currentYear}"
    # else:
    #     chartTitle = "Total Expenses All"
    
    #chart json
    chart = {
        'chart': {'type': 'sankey','renderTo':'expenses-sankey-container'},
        'title': {'text': chartTitle},
        'tooltip': {
        'headerFormat': None,
        'pointFormat':
      '{point.fromNode.name} \u2192 {point.toNode.name}: ${point.weight:.2f}',
        'nodeFormat': '{point.name}: ${point.sum:.2f}'
    },
        'series': [{
            'name':'Amount',
            'keys':['from','to','weight'],
            'nodes': [
                {
                    'id':'Income',
                    'color':'#adf5a1'
                },
                {
                    'id':'Savings',
                    'color':'#adf5a1'
                },
                {
                    'id':'Expenses',
                    'color':'#ff7676'
                },
                {
                    'id':'GROCERIES',
                    'color':'#ff7676'
                },
                {
                    'id':'GAS_REPAIRS',
                    'color':'#ff7676'
                },
                {
                    'id':'DINE_OUT',
                    'color':'#ff7676'
                },
                {
                    'id':'RENT_MORTGAGE',
                    'color':'#ff7676'
                },
                {
                    'id':'TAXES',
                    'color':'#ff7676'
                },
                {
                    'id':'UTILITIES',
                    'color':'#ff7676'
                },
                {
                    'id':'GIVING',
                    'color':'#ff7676'
                },
                {
                    'id':'HEALTHCARE',
                    'color':'#ff7676'
                },
                {
                    'id':'HOME_IMPROVEMENT',
                    'color':'#ff7676'
                },
                {
                    'id':'SHOPPING',
                    'color':'#ff7676'
                },
                {
                    'id':'TRAVEL',
                    'color':'#ff7676'
                },
                {
                    'id':'ENTERTAINMENT',
                    'color':'#ff7676'
                },
            ],
            'data': data,
            'type':'sankey',
        }]
    }
    
    return JsonResponse(chart)
