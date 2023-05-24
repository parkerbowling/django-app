from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home_view(request):
    #return HttpResponse("<h1>Hello World</h1>")
    return render(request, "home.html", {})

def contact_view(request,*args, **kwargs):
    return render(request, "contact.html", {})

def about_view(request, *args, **kwargs):
    my_context = {
        "my_text": "This is About US",
        "my_number": 123,
        "my_list": [1,2,3,4,5,6]
    }
    return render(request, "about.html", my_context)

def social_view(*args, **kwargs):
    return HttpResponse("<h1>Social View</h1>")