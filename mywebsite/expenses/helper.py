from .models import expenseReport

#Helper Functions
def getExpenseCategories(rList):
    #get category names, should these be helper functions?
    setCategories = expenseReport.objects.values("expenseChoices")
    rList = list(set([i[1] for s in [d.items() for d in setCategories] for i in s]))
    
    return rList
