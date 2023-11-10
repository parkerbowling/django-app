from django.shortcuts import redirect, render
from django.db.models import Sum
from .models import expenseReport
from .forms import expenseReportForm, expenseComparison
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
import json
from . import helper as h
from pandas import period_range
from numpy import average as avg

#temporary home page for now
def home(request):
    #render takes in a request and an HTML page to render to view
    return render(request, 'home.html')

def expense_home(request):
    
    if request.method == "GET":
        
        #initalize empty form (figure out how to preload an inital value?)
        formFilter = expenseComparison()

    else:
        #get date on a POST
        formFilter = expenseComparison(request.POST)
        
        if formFilter.is_valid():

            #get data from cleaned, valid form
            fromDateData = formFilter.cleaned_data['date']
            toDateData = formFilter.cleaned_data['toDate']
            categoryFilterData = formFilter.cleaned_data['expenseLabelCategory'] 
                        
            #From date data
            obj = json.dumps(fromDateData, indent=4, sort_keys=True, default=str)
            request.session['date'] = obj  #formFilter.cleaned_data['date']

            #To date data
            obj1 = json.dumps(toDateData, indent=4, sort_keys=True, default=str)
            request.session['toDate'] = obj1
            
            #filter category
            obj2 = categoryFilterData
            request.session['expenseLabelCategory'] = obj2
            
    
    context = {
        "form":formFilter
    }
    
    return render(request,'expense_home.html', context)

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

def expense_piechart(request):
    
    #dynamically get the Categories in case I decide to add or remove one of them and make them unique
    newSet = []
    newSet = h.getExpenseCategories()
    try:
        newSet.remove("INCOME")
    except ValueError:
        print("no income reported")
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
        'chart': {
            'type': 'pie', 
            # 'height': 300,
            # 'width': 1000,
            'renderTo':'expenses-pie-container'
        },
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

def expense_sankeychart(request):
    
    #get category names, should these be helper functions?
    newSet = []
    newSet = h.getExpenseCategories()
    try:
        newSet.remove("INCOME")
    except ValueError:
        print("no income reported")

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
        chartTitle = f"Expenses and Savings This Month {currentMonth}/{currentYear}"
    # else:
    #     chartTitle = "Total Expenses All"
    
    #chart json
    chart = {
        'chart': {
            'type': 'sankey',
            'renderTo':'expenses-sankey-container',
            # 'height': 300,
            # 'width': 1000,
        },
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

def expense_comparison_barchart(request):
    newSet = []
    newSet = h.getExpenseCategories()
    try:
        newSet.remove("INCOME")
    except ValueError:
        print("no income reported")
    
    #gets the date input from the user (STILL NEED THIS TO BE AUTOMATICALLY CHANGED ON FILTER CHANGE)
    fromDate = request.session.get("date")
    fromDate = fromDate.split("-")
    fromYear = fromDate[0].strip('"')
    fromMonth = fromDate[1]
    fromDay = fromDate[2].strip('"')
    
    #get toDate
    toDate = request.session.get("toDate")
    toDate = toDate.split("-")
    toYear = toDate[0].strip('"')
    toMonth = toDate[1]
    toDay = toDate[2].strip('"')
    
    #get category
    filterCategory = request.session.get("expenseLabelCategory")
    
    #title
    chartTitle = "Comparison Chart"
    
    #initalize for chart json
    data = []
     
    #get list of months from range input
    month_list = period_range(start=f"{fromYear}-{fromMonth}-{fromDay}", end=f"{toYear}-{toMonth}-{toDay}", freq='M')
    month_list = [month.strftime("%m-%Y") for month in month_list]
    categoryLabelList = month_list
    
    #do something if only one category is requested
    if filterCategory != "All Expenses" and filterCategory != "Savings":
    
        #data for each bar
        bar = {
            "name":filterCategory,
            "type":'column',
            "data":[]
        }
        
        #date for average
        average = {
            'type': 'spline',
            'name': 'Average',
            'data': []
        }   
        
        listOfDataSum = []
            
        #for each month
        for d in month_list:
            
    #       get the sum of the category and store in a list        
            dataSum = expenseReport.objects.values("value"
                    ).filter(
                        date__year=d[3:], date__month=d[:2]
                    ).filter(
                        expenseChoices=str(filterCategory)).aggregate(
                    Sum('value'))['value__sum']
            
            if dataSum == None:
                dataSum = 0.0
                        
            listOfDataSum.append(float(dataSum))
            
        #compute average of sums of categories    
        bar["data"] = listOfDataSum
        average["data"] = [avg(listOfDataSum) for i in range(len(listOfDataSum))]
        data.append(bar)
        data.append(average)
    
    #this needs work!
    elif filterCategory == "Savings":

        bar = {
            "name":filterCategory,
            "type":'column',
            "data":[]
        }
        
        #date for average
        average = {
            'type': 'spline',
            'name': 'Average',
            'data': []
        }         

        listOfDataSum = []
        allThings = []
             
        #for each expense category
        for c in newSet:
            
            bar = {
                "name":'Savings',
                "type":'column',
                "data":[]
            }
            
            listOfDataSum = []

        savingsList = h.getAllExpenses_SavingsInMonthRange(month_list)
            
        bar['data'] = savingsList
        data.append(bar)
        average['data'] = [avg(savingsList) for i in range(len(savingsList))]
        data.append(average)
    
    else: #for all expenses
        
        #average data (still need to implement this)
        average = {
            'type': 'spline',
            'name': 'Average',
            'data': []
        }


        #for each expense category
        for c in newSet:
            
            bar = {
                "name":c,
                "type":'column',
                "data":[]
            }
            
            listOfDataSum = []
            
            #for each month, get the sums
            for d in month_list:
                
                #get the sum of the category and store in a list        
                dataSum = expenseReport.objects.values("value"
                        ).filter(
                            date__year=d[3:], date__month=d[:2]
                        ).filter(
                            expenseChoices=str(c)).aggregate(
                        Sum('value'))['value__sum']
                
                if dataSum == None:
                    dataSum = 0.0
                    #do I need this 'continue'? Maybe not, but maybe it is better without it
                    #continue
                           
                listOfDataSum.append(float(dataSum))
                
        
            bar['data'] = listOfDataSum
            data.append(bar)
            
        listoftotalexpenses = []
        
        for d in month_list:
            
            totalPerMonth = 0
            
            for c in newSet:
                dataSum = expenseReport.objects.values("value"
                    ).filter(
                        date__year=d[3:], date__month=d[:2]
                    ).filter(
                        expenseChoices=str(c)).aggregate(
                    Sum('value'))['value__sum']
            
                if dataSum == None:
                    dataSum = 0.0
                    #do I need this 'continue'? Maybe not, but maybe it is better without it
                    #continue
                
                totalPerMonth += float(dataSum)
            
            listoftotalexpenses.append(totalPerMonth)
        
        
        print(listoftotalexpenses)
        average["data"] = [avg(listoftotalexpenses) for i in range(len(listoftotalexpenses))]
        data.append(average)
            
    #get average of each month and not total
    #Need to do these before MD
    #1. Average for all expenses
    #2. credit card chart
    #3. Better display for recipes
    #4. Edit expense categories-> make gas separate and put car expenses with Home improvement
            
    average = {
            'type': 'spline',
            'name': 'Average',
            'data': []
        }   
    
    chart = {
        "chart": {
            "type": 'column',
            'renderTo':'expenses-comparison-container',
        },
        "title": {
            "text": chartTitle, 
        },
        "xAxis": {
            "categories": categoryLabelList,
            "crosshair": "true",
        },
        "yAxis": {
            "min": 0,
            "title": {
                "text": 'Dollars'
            }
        },
        "tooltip": {
            'headerFormat': None,
            'valueSuffix':'Dollars',
            'pointFormat':
                '{series.name}: ${point.y:.2f}',
        },
        "plotOptions": {
            "column": {
                "pointPadding": 0.2,
                "borderWidth": 0
            }
        },
        "series": data
    }
    
    
    return JsonResponse(chart)
    