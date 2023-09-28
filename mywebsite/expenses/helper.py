from .models import expenseReport

#Helper Functions
def getExpenseCategories(option=None):
    #get category names, should these be helper functions?
    rList = []
    setCategories = expenseReport.objects.values("expenseChoices")
    rList = list(set([i[1] for s in [d.items() for d in setCategories] for i in s]))
    
    if option == "all":
        rList.append("All Expenses")
    
    return rList
