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
    path('comparison-chart-category-data/<str:category>/<str:date>/',views.comparison_chart_category_data,name='comparison-chart-category-data'),
    #path('add/', views.add_budget_category, name='add_budget_category'),  # Add this URL pattern for handling form submission
    #path('manage/', views.manage_budget_categories, name='manage_budget_categories'),
    #path('edit/<int:pk>/', views.edit_budget_category, name='edit_budget_category'),
    #path('delete/<int:pk>/', views.delete_budget_category, name='delete_budget_category'),
    path('budget/modal/', views.budget_modal_view, name='budget_modal_view'),
    path('budget/save/', views.save_budget_category_view, name='save_budget_category'),
    path('budget/edit/<int:category_id>/', views.edit_category_view, name='edit_category'),
    path('budget/delete/<int:category_id>/', views.delete_category_view, name='delete_category'),
    path('budget/edit/save/<int:category_id>/',views.save_budget_category_view_with_id,name='save_budget_category_view'),
    
    
]