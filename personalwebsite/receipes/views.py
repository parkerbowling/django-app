from django.shortcuts import redirect, render, get_object_or_404
from .models import receipesModel
from .forms import receipesForm
from django.contrib import messages

def add_receipe(request):
    form = receipesForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            print("do we get here")
            form.save()
            messages.success(request,"Receipe Added!")
            return redirect('receipes:add_receipe')
        
    context = {
        "form":form
    }
    return render(request, 'add_receipe.html',context)