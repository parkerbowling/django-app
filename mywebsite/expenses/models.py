from django.db import models
from django.utils.timezone import now

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    
class BudgetCategory(models.Model):
    name = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10,decimal_places=0,null=True, blank=True)
    #cashBack = models.DecimalField(max_digits=6,decimal_places=2,null=True,blank=True)

    def __str__(self):
        return self.name

def get_or_create_default_category():
    category, created = BudgetCategory.objects.get_or_create()
    #category_data = {'name': category.name, 'value': str(category.value)}
    return category

#See forms.py for more details
class expenseReport(models.Model):    
    
    #see forms for more details
    date = models.DateField(default=now)
    title = models.CharField(max_length=128)
    category = models.ForeignKey(BudgetCategory, on_delete=models.CASCADE,   related_name='expense_reports')
    value = models.DecimalField(decimal_places=2, max_digits=1000)
    note = models.TextField(max_length=140)

    def __str__(self):
        return self.title
    

    