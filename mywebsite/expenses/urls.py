from django.urls import path
from . import views

#defines the app name for a namespace to be used in personalwebsite/urls.py
app_name = 'expenses'

#the url pattern that links expenses/add_expense to personalwebsite/urls.py
urlpatterns = [
    path('expense_home/',views.expense_home, name='expense_home'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('json-example/data/',views.chart_data, name='chart_data'),
    path('sankey-chart',views.sankey_chart,name='sankey_chart')
]