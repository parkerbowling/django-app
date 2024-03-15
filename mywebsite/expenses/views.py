from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum
from .models import expenseReport, BudgetCategory
from .forms import expenseReportForm, expenseComparison, BudgetCategoryForm, ExpenseCategory
from django.template.loader import render_to_string
from django.core.serializers import serialize
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


def budget_chart_data(request):
    budget_categories = list(BudgetCategory.objects.all())
    print(budget_categories)
    print(budget_categories[0].value)
    date_now = datetime.now()
    current_year = date_now.year
    current_month = date_now.month
    title = f'Monthly Budget for {current_month}/{current_year}'

    data_of_expenses = []

    for cat in budget_categories:
        category_sum = expenseReport.objects.values("value").filter(
            date__year=current_year, date__month=current_month
        ).filter(
            category__name=str(cat)
        ).aggregate(
            Sum('value')
        )['value__sum'] or 0

        data_of_expenses.append(float(category_sum))

    # something is wrong here, need to rethink
    # the order of the categories is not right
    sorted_indices = sorted(range(len(data_of_expenses)), key=lambda x: data_of_expenses[x])
    budget_categories = [budget_categories[i] for i in sorted_indices]
    data_of_expenses = [data_of_expenses[i] for i in sorted_indices]

    # Extract numeric values from BudgetCategory instances
    try:
        budget_values = [float(category.value) for category in budget_categories]
    except TypeError:
        print("There are null values, oh no!")
        budget_values = []
    print("Theses are the budget_values before json serialized: ",budget_values)
    
    # Convert budget_values to a JSON-serializable list
    budget_values_json = list(map(float, budget_values))
    print("These are the values after: ",budget_values_json)

    final_data = {
        'categories': [category.name for category in budget_categories],
        'budget_values': budget_values_json,
        'title': title,
        'series': [
            {'name': 'Alloted Budget Amount', 'data': budget_values_json, 'color': '#A1E097'},
            {'name': 'Expense Amount', 'data': data_of_expenses, 'color': '#F56C6C'}
        ]
    }

    return JsonResponse(final_data)
   
##############################  

def budget_modal_view(request):
    categories = BudgetCategory.objects.all()
    form = BudgetCategoryForm()
    print("in the budget modal view")
    return render(request, 'budget_modal.html', {'form': form, 'categories': categories})

def debug(request):
    categories = BudgetCategory.objects.all()
    form = BudgetCategoryForm()
    return render(request, 'delete_budget_category_form.html', {'form': form})

def save_budget_category_view(request):
    if request.method == 'POST':
        form = BudgetCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        # For GET requests, return an empty form
        form = BudgetCategoryForm()
        return render(request, 'budget_modal_form.html', {'form': form})

def edit_category_view(request, category_id):
    category = get_object_or_404(BudgetCategory, id=category_id)

    if request.method == 'POST':
        form = BudgetCategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            # Serialize the category and send it as JSON
            serialized_category = serialize('json', [category])
            return JsonResponse({'success': True, 'category': serialized_category})
        else:
            return JsonResponse({'error': form.errors}, status=400)

    return render(request, 'edit_budget_category_form.html', {'form': BudgetCategoryForm(instance=category)})

def delete_category_view(request, category_id):
    # Retrieve the instance of BudgetCategory or return a 404 response
    category = get_object_or_404(BudgetCategory, id=category_id)

    try:
        # Attempt to delete the BudgetCategory instance
        category.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        print("exception!")
        # If an exception occurs, return an error response with details
        return JsonResponse({'error': f'Delete failed: {str(e)}'}, status=500)

#################################

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

def pie_chart_category_data(request, category):
    print(category)
    
    dateNow = datetime.now()
    currentYear = dateNow.year
    currentMonth = dateNow.month
    
    categorySum = expenseReport.objects.values("date","title","value"
                    ).filter(
                        date__year=currentYear, date__month=currentMonth
                    ).filter(
                        category__name=str(category))
                    
    return JsonResponse(list(categorySum), safe=False)

def pie_chart_data(request):
        #dynamically get the Categories in case I decide to add or remove one of them and make them unique
    newSet = list(BudgetCategory.objects.all())
    for i in range(len(newSet)):
        newSet[i] = newSet[i].name
    try:
        newSet.remove("Income")
    except ValueError:
        print("no income reported")
    #name a json structure for inserting data into chart
    allCategoryData = {
        "title": "",
        "data": [],
    }
    
    dataForAll = []
    
    #for every category (remember not all categories may have appeared yet) sum the values and add to data
    #will need to be able to filter on certain dates, like months and years
    dateNow = datetime.now()
    currentYear = dateNow.year
    currentMonth = dateNow.month
    
    allCategoryData["title"] = f"Expenses for {currentMonth}/{currentYear}"
    
    for i in newSet:
        
        #gets all values for category and sums
        if True:
            categorySum = expenseReport.objects.values("value").filter(
            date__year=currentYear, date__month=currentMonth
            ).filter(
                category__name=str(i)
            ).aggregate(
                Sum('value')
            )['value__sum'] or 0
                        
        #if there is no data, no need to add to chart     
        if categorySum == 0:
            continue

        data = {
            'name':str(i),
            'y': float(categorySum)
        }
        
        dataForAll.append(int(categorySum))

        allCategoryData['data'].append(data)
         
    return JsonResponse(allCategoryData, safe=False)

#
# Pie Chart
#
def expense_piechart(request):
    return

#
# Sankey Chart
#
def expense_sankeychart(request):
    
    #get category names, should these be helper functions?
    newSet = list(BudgetCategory.objects.all())
    for i in range(len(newSet)):
        newSet[i] = newSet[i].name
    try:
        newSet.remove("Income")
    except ValueError:
        print("no income reported")

    data = []
    
    #get current dates
    dateNow = datetime.now()
    currentYear = dateNow.year
    currentMonth = dateNow.month
    
    #get the income total
    incomeSum = expenseReport.objects.values("value").filter(
            date__year=currentYear, date__month=currentMonth
        ).filter(
            category__name=str("Income")
        ).aggregate(
            Sum('value')
        )['value__sum'] or 0
    
    #check for no income SHOULDN"T NEED THIS         
    # if incomeSum == None:
    #     incomeSum = 0
               
    #get all expenses  
    expensesSum = 0  
    expensesDict = {}
                       
    for i in newSet:
        categorySum = expenseReport.objects.values("value").filter(
                date__year=currentYear, date__month=currentMonth
            ).filter(
                category__name=str(i)
            ).aggregate(
                Sum('value')
            )['value__sum'] or 0
        if categorySum == None:
            continue
        
        expensesDict[i] = float(categorySum)
        
        expensesSum += float(categorySum)
        
    #calculate income and savings
    incomeSum = float(incomeSum)
    savingsSum = incomeSum - expensesSum
    
    #if this is a negative number, make it zero for the chart - might need to skip it
    if savingsSum < 0:
        savingsSum = 0
        
    #append for json file                
    data.append(
        ['Income','Savings',savingsSum,'#adf5a1']
    )
    data.append(
        ['Income','Expenses',expensesSum,'#adf5a1']
    )

    for index, key in expensesDict.items():
        data.append(
            ['Expenses',index,key,'#ff7676']
        )

    #add if else when chart wants to be changed
    chartTitle = ""
    if True:
        chartTitle = f"Expenses and Savings This Month {currentMonth}/{currentYear}"
    # else:
    #     chartTitle = "Total Expenses All"
    
    #make the Nodes list here, so it's dynamic
    nodeColors = []

# Iterate over the category IDs and create a dictionary for each node
    for category_id in newSet:
        node = {
            'id': category_id,
            'color': '#ff7676'  # You can set color dynamically based on some condition if needed
        }
        nodeColors.append(node)
    
    nodeColors.append({'id': 'Savings','color': '#adf5a1'})
    nodeColors.append({'id': 'Income','color': '#adf5a1'})
    nodeColors.append({'id': 'Expenses','color': '#ff7676'})
    
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
            'keys':['from','to','weight','color'],
            'nodes': nodeColors,
            'data': data,
            'type':'sankey',
        }]
    }
    


    #return JsonResponse({'data':'none'})
    return JsonResponse(chart)

def comparison_chart_category_data(request,cat,date):
    print("THIS IS THE DATE", date)

    
    if date == None:
        dateNow = datetime.now()
        currentYear = dateNow.year
        currentMonth = dateNow.month
    else:
        currentMonth = int(date[:2])
        currentYear = int(date[3:7])
    
    categorySum = expenseReport.objects.values("date","title","value"
                    ).filter(
                        date__year=currentYear, date__month=currentMonth
                    ).filter(
                        category=str(cat)) or 0
                    
    return JsonResponse(list(categorySum), safe=False)

def expense_comparison_barchart(request):

    newSet = list(BudgetCategory.objects.all())
    for i in range(len(newSet)):
        newSet[i] = newSet[i].name
    try:
        newSet.remove("Income")
    except ValueError:
        print("no income reported")
    
    #gets the date input from the user
    fromDate = request.session.get("date") #on first start this has no value, need to chaange this to a try statement
   
        #get current dates
    dateNow = datetime.now()
    currentYear = dateNow.year
    currentMonth = dateNow.month
   
    if fromDate == None:
        print("Argggggggg")
        date_now = datetime.now()
        currentYear = date_now.year
        currentMonth = date_now.month
        currentDay = date_now.day
        
        month_list = period_range(start=f"{currentYear}-{currentMonth}-01", end=f"{currentYear}-{currentMonth}-{currentDay}", freq='M')
        month_list = [month.strftime("%m-%Y") for month in month_list]
        categoryLabelList = month_list
   
    else:
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
        
            #get list of months from range input
        month_list = period_range(start=f"{fromYear}-{fromMonth}-{fromDay}", end=f"{toYear}-{toMonth}-{toDay}", freq='M')
        month_list = [month.strftime("%m-%Y") for month in month_list]
        categoryLabelList = month_list
    
    #get category
    filterCategory = request.session.get("expenseLabelCategory")
 
    
    #check checkbox value
    checkbox = request.session.get("checkbox")
    #print(checkbox)
    
    #title
    chartTitle = "Comparison Chart"
    
    #initalize for chart json
    data = {
        "categories":[],
        "series":[]
    }
     
    data['categories'] = categoryLabelList
    
    #do something if only one category is requested
    if filterCategory != "All Expenses" and filterCategory != "Savings":
        
        seriesData = []
    
        #data for each bar
        bar = {
            "name":filterCategory,
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
        print(month_list)
        for d in month_list:
            
    #get the sum of the category and store in a list        
            dataSum = expenseReport.objects.values("value"
                    ).filter(
                        date__year=d[3:], date__month=d[:2]
                    ).filter(
                        category=str(filterCategory)).aggregate(
                    Sum('value'))['value__sum'] or 0
            
            if dataSum == None:
                dataSum = 0.0
            print(dataSum)
            listOfDataSum.append(float(dataSum))
            
        #compute average of sums of categories    
        bar["data"] = listOfDataSum
        average["data"] = [avg(listOfDataSum) for i in range(len(listOfDataSum))]
        seriesData.append(bar)
        seriesData.append(average)
        data['series'] = seriesData
    
    #this needs work!
    elif filterCategory == "Savings":

        seriesData = []

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
                "data":[]
            }
            
            listOfDataSum = []

        savingsList = h.getAllExpenses_SavingsInMonthRange(month_list)
            
        bar['data'] = savingsList
        seriesData.append(bar)
        average['data'] = [avg(savingsList) for i in range(len(savingsList))]
        seriesData.append(average)
        data['series'] = seriesData
    
    else: #for all expenses
        
        seriesData = []
        
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
            seriesData.append(bar)
        
        listoftotalexpenses = []
        
        #I think this is for the average line, need to actually implement
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
        
        data['series'] = seriesData
        #print(listoftotalexpenses)
    return JsonResponse(data, safe=False)
    