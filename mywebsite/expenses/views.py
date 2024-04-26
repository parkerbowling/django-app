from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Sum
from .models import expenseReport, BudgetCategory
from .forms import expenseReportForm, expenseComparison, BudgetCategoryForm, ExpenseCategory
from django.contrib import messages
from django.http import JsonResponse
from datetime import datetime
from pandas import period_range
from numpy import average as avg
from django.contrib.auth.decorators import login_required

#temporary home page for now
@login_required
def home(request):
    #render takes in a request and an HTML page to render to view
    return render(request, 'home.html')

@login_required
def budget_chart_data(request):
    budget_categories = list(BudgetCategory.objects.filter(user=request.user))
    for i in budget_categories:
        if i.name == "Income":
            budget_categories.remove(i)
    date_now = datetime.now()
    current_year = date_now.year
    current_month = date_now.month
    title = f'Monthly Budget for {current_month}/{current_year}'

    data_of_expenses = []

    for cat in budget_categories:
        
        if cat == "Income":
            continue
        
        category_sum = expenseReport.objects.values("value").filter(user=request.user,
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
    
    # Convert budget_values to a JSON-serializable list
    budget_values_json = list(map(float, budget_values))

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
@login_required
def budget_modal_view(request):
    #categories = BudgetCategory.objects.all()
    categories = list(BudgetCategory.objects.filter(user=request.user))
    for i in categories:
        if i.name == "Income":
            categories.remove(i)
    form = BudgetCategoryForm(request.user)
    return render(request, 'budget_modal.html', {'form': form, 'categories': categories})

@login_required
def save_budget_category_view_with_id(request, category_id):
    if request.method == 'POST':
        # Process POST request
        form = BudgetCategoryForm(request.POST)
        if form.is_valid():
            # Retrieve the category instance based on the provided category ID
            category = get_object_or_404(BudgetCategory, id=category_id)

            # Update the category instance with the submitted form data
            category.name = form.cleaned_data['name']
            print("CATEGORY NAME AND VALUE",category.name,category.value)
            category.value = form.cleaned_data['value']
            # Update other fields as needed

            # Save the changes to the category
            category.save()

            # Return a success JSON response
            return JsonResponse({'success': True})
        else:
            # Return a JSON response with form errors
            return JsonResponse({'errors': form.errors}, status=400)
    elif request.method == 'GET':
        # Handle GET request to render the form
        category = get_object_or_404(BudgetCategory, id=category_id)
        form = BudgetCategoryForm(instance=category)  # Populate form with existing category data
        return render(request, 'edit_budget_category_form.html', {'form': form})
    else:
        # Handle other HTTP methods (e.g., PUT, DELETE)
        return JsonResponse({'error': 'Method Not Allowed'}, status=405)

@login_required
def save_budget_category_view(request):
    if request.method == 'POST':
        form = BudgetCategoryForm(data=request.POST,user=request.user)
        form.save()
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': form.errors}, status=400)
    else:
        # For GET requests, return an empty form
        form = BudgetCategoryForm(user=request.user)
        return render(request, 'budget_modal.html', {'form': form})

@login_required
def edit_category_view(request, category_id=None):
    if category_id:
        # Retrieve the existing instance if category_id is provided
        category = get_object_or_404(BudgetCategory, id=category_id)
    else:
        category = None

    if request.method == 'POST':
        # Handle form submission
        form = BudgetCategoryForm(data=request.POST, user=request.user,instance=category)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        # Render the form with existing instance data or empty form
        form = BudgetCategoryForm(user=request.user,instance=category)
        return render(request, 'edit_budget_category_form.html', {'form': form, 'category': category})

@login_required
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
@login_required
def expense_home(request):
    
    if request.method == "GET":
        
        #initalize empty form (figure out how to preload an inital value?)
        formFilter = expenseComparison(user=request.user)

    else:
        #get date on a POST
        formFilter = expenseComparison(data=request.POST,user=request.user)
        
        if formFilter.is_valid():
            #get data from cleaned, valid form
            
            form_data = formFilter.cleaned_data
            
            category_name = form_data['expenseLabelCategory'].name if form_data['expenseLabelCategory'] else None

            # Serialize form data to JSON
            serialized_data = {
                'date': form_data['date'].strftime('%Y-%m-%d'),
                'toDate': form_data['toDate'].strftime('%Y-%m-%d'),
                'expenseLabelCategory': category_name,
                'checkbox': form_data['checkbox'],
            }
                        
            #From date data
            request.session['date'] = serialized_data['date']    #obj

            #To date data
            request.session['toDate'] = serialized_data['toDate']   #obj1
            
            #filter category
            request.session['expenseLabelCategory'] = serialized_data['expenseLabelCategory'] #obj2
        
        else:
            
            form_data = formFilter.cleaned_data
            
            expense_label_category = request.POST.get('expenseLabelCategory', 'default_category')
            
            serialized_data = {
                'date': form_data['date'].strftime('%Y-%m-%d'),
                'toDate': form_data['toDate'].strftime('%Y-%m-%d'),
                'expenseLabelCategory': expense_label_category,
                'checkbox': form_data['checkbox'],
            }
                        
            #From date data
            request.session['date'] = serialized_data['date']    #obj

            #To date data
            request.session['toDate'] = serialized_data['toDate']   #obj1
            
            #filter category
            request.session['expenseLabelCategory'] = serialized_data['expenseLabelCategory'] #obj2
            
    
    extra_choices = [
        ('Savings', 'Savings'),
        ('All Expenses', 'All Expenses'),
        # Add more extra choices as needed
    ]
    
    formFilter.fields['expenseLabelCategory'].choices = list(formFilter.fields['expenseLabelCategory'].choices) + extra_choices
    
    context = {
        "form":formFilter
    }
    
    return render(request,'expense_home.html', context)

#add_expense is the page where user can add expense
@login_required
def add_expense(request):

    #define a form to be used. Arguments POST it to the view if a POST is requested or post an empty form
    
    if request.method == "GET":
        
        #initalize empty form (figure out how to preload an inital value?)
        form = expenseReportForm(user=request.user)

    #if the method is a POST, save form and return success and redirect to a new form
    else:
        form = expenseReportForm(data=request.POST,user=request.user)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense added!')
            return redirect('expenses:add_expense')
        
    #context allows variables to be passed into the HTML file, see HTML file named below
    context = {
        "form":form
    }
    return render(request, 'add_expense.html', context)

@login_required
def pie_chart_category_data(request, category):
    
    dateNow = datetime.now()
    currentYear = dateNow.year
    currentMonth = dateNow.month
    
    categorySum = expenseReport.objects.values("date","title","value"
                    ).filter(
                        date__year=currentYear, date__month=currentMonth,user=request.user
                    ).filter(
                        category__name=str(category))
                    
    return JsonResponse(list(categorySum), safe=False)

@login_required
def pie_chart_data(request):
        #dynamically get the Categories in case I decide to add or remove one of them and make them unique
    newSet = list(BudgetCategory.objects.filter(user=request.user))
    for i in range(len(newSet)):
        newSet[i] = newSet[i].name
        
    newSet.remove('Income')
    print(newSet)
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
            date__year=currentYear, date__month=currentMonth,user=request.user
            ).filter(
                category__name=str(i)
            ).filter(
                user=request.user
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
@login_required
def expense_piechart(request):
    return

#
# Sankey Chart
#
@login_required
def expense_sankeychart(request):
    
    #get category names, should these be helper functions?
    newSet = list(BudgetCategory.objects.filter(user=request.user))
    for i in range(len(newSet)):
        newSet[i] = newSet[i].name
    
    newSet.remove('Income')
    print(newSet)
    data = []
    
    #get current dates
    dateNow = datetime.now()
    currentYear = dateNow.year
    currentMonth = dateNow.month
    
    #get the income total
    incomeSum = expenseReport.objects.values("value").filter(
            date__year=currentYear, date__month=currentMonth,user=request.user
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
                date__year=currentYear, date__month=currentMonth,user=request.user
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

@login_required
def comparison_chart_category_data(request,category,date):
    
    if date == None:
        dateNow = datetime.now()
        currentYear = dateNow.year
        currentMonth = dateNow.month
    else:
        currentMonth = int(date[:2])
        currentYear = int(date[3:7])
    
    categorySum = expenseReport.objects.values("date","title","value"
                    ).filter(
                        date__year=currentYear, date__month=currentMonth,user=request.user
                    ).filter(
                        category__name=str(category)) #or 0
                    
    return JsonResponse(list(categorySum), safe=False)

@login_required
def expense_comparison_barchart(request):

    newSet = list(BudgetCategory.objects.filter(user=request.user))
    for i in range(len(newSet)):
        newSet[i] = newSet[i].name
        
    print(newSet)
    
    #gets the date input from the user
    fromDate = request.session.get("date") #on first start this has no value, need to chaange this to a try statement
   
        #get current dates
    dateNow = datetime.now()
    currentYear = dateNow.year
    currentMonth = dateNow.month
   
    if fromDate == None:
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
    if filterCategory == None:
        filterCategory = "Income"
    
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
        for d in month_list:
            
            #get the sum of the category and store in a list        
            dataSum = expenseReport.objects.values("value"
                    ).filter(
                        date__year=d[3:], date__month=d[:2],user=request.user
                    ).filter(
                        category__name=str(filterCategory)).aggregate(
                    Sum('value'))['value__sum'] or 0
            
            if dataSum == None:
                dataSum = 0.0
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
        
    #for each month
        for d in month_list:
            
            totalExpenses = 0
            
            for e in newSet:
                    
        #       get the sum of the category and store in a list        
                dataSum = expenseReport.objects.values("value"
                        ).filter(
                            date__year=d[3:], date__month=d[:2],user=request.user
                        ).filter(
                            category__name=str(e)).aggregate(
                        Sum('value'))['value__sum']
                
                if dataSum == None:
                    dataSum = 0.0
                    
                totalExpenses += float(dataSum)
                
            totalSavings = totalExpenses
                    
            incomeBal = expenseReport.objects.values("value"
                    ).filter(
                        date__year=d[3:], date__month=d[:2],user=request.user
                    ).filter(
                        category__name=str("Income")).aggregate(
                    Sum('value'))['value__sum'] or 0
        
            
            #savings = income - expenses
            totalSavings = float(incomeBal) - float(totalSavings)
            
            listOfDataSum.append(totalSavings)
        
        for i in range(len(listOfDataSum)):
            listOfDataSum[i] = round(listOfDataSum[i],2)
        
        savingsList = listOfDataSum
        
################################################
                
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
                            date__year=d[3:], date__month=d[:2],user=request.user
                        ).filter(
                            category__name=str(c)).aggregate(
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
                        date__year=d[3:], date__month=d[:2],user=request.user
                    ).filter(
                        category__name=str(c)).aggregate(
                    Sum('value'))['value__sum']
            
                if dataSum == None:
                    dataSum = 0.0
                    #do I need this 'continue'? Maybe not, but maybe it is better without it
                    #continue
                
                totalPerMonth += float(dataSum)
            
            listoftotalexpenses.append(totalPerMonth)
        
        data['series'] = seriesData

    return JsonResponse(data, safe=False)
    