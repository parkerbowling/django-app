from django.urls import path
from . import views

#defines the app name for a namespace to be used in personalwebsite/urls.py
app_name = 'expenses'

#the url pattern that links expenses/add_expense to personalwebsite/urls.py
urlpatterns = [
    path('expense_home/',views.expense_home, name='expense_home'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('pie-chart/',views.expense_piechart, name='expense_piechart'),
    path('sankey-chart/',views.expense_sankeychart,name='expense_sankeychart'),
    path('comparison-chart/',views.expense_comparison_barchart,name='expense_comparison_barchart'),
]