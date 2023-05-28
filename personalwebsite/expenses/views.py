from django.shortcuts import redirect, render, get_object_or_404
from .models import expenseReport
from .forms import expenseReportForm
from django.contrib import messages

def home(request):
    queryset = expenseReport.objects.all().order_by('-date')
    context = {
        'queryset': queryset
    }
    return render(request, 'home.html', context)

def add_expense(request):

    form = expenseReportForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, 'Expense added!')
            return redirect('expenses:add_expense')
        
    context = {
        "form":form
    }
    return render(request, 'add_expense.html', context)

