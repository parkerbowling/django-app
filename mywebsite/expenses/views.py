from django.shortcuts import redirect, render, get_object_or_404
from .models import expenseReport
from .forms import expenseReportForm
from django.contrib import messages

#temporary home page for now
def home(request):
    #render takes in a request and an HTML page to render to view
    return render(request, 'home.html')

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

