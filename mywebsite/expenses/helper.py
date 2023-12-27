from .models import expenseReport
from django.db.models import Sum

#Helper Functions
def getExpenseCategories(option=None):
    #get category names, should these be helper functions?
    rList = []
    setCategories = expenseReport.objects.values("expenseChoices")
    rList = list(set([i[1] for s in [d.items() for d in setCategories] for i in s]))
    
    if option == "all":
        rList.append("All Expenses")
        rList.append("Savings")
    
    return rList


def getAllExpenses_SavingsInMonthRange(month_list):

    #get all expenses for each month    
    listOfExpenseCategories = getExpenseCategories()
    listOfExpenseCategories.remove("INCOME")

    listOfDataSum = []
        
    #for each month
    for d in month_list:
        
        totalExpenses = 0
        
        for e in listOfExpenseCategories:
                
    #       get the sum of the category and store in a list        
            dataSum = expenseReport.objects.values("value"
                    ).filter(
                        date__year=d[3:], date__month=d[:2]
                    ).filter(
                        expenseChoices=str(e)).aggregate(
                    Sum('value'))['value__sum']
            
            if dataSum == None:
                dataSum = 0.0
                
            totalExpenses += float(dataSum)
            
        totalSavings = totalExpenses
                
        incomeBal = expenseReport.objects.values("value"
                ).filter(
                    date__year=d[3:], date__month=d[:2]
                ).filter(
                    expenseChoices=str("INCOME")).aggregate(
                Sum('value'))['value__sum']
        
        if incomeBal == None:
            incomeBal = 0.0   
        
        #savings = income - expenses
        totalSavings = float(incomeBal) - float(totalSavings)
        
        listOfDataSum.append(totalSavings)
    
    for i in listOfDataSum:
        i = round(i,2)
    
    return listOfDataSum
    