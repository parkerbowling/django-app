from django.shortcuts import redirect, render, get_object_or_404
from .models import expenseReport
from .forms import expenseReportForm

def home(request):
    queryset = expenseReport.objects.all().order_by('-date')
    context = {
        'queryset': queryset
    }
    return render(request, 'app/base.html', context)

def create(request):
    form = expenseReportForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect ('home')
    context = {
        "form":form
    }
    return render(request, 'app/create.html', context)
