from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from expenses.models import BudgetCategory
from expenses.forms import BudgetCategoryForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('initial-setup')  # Redirect to add budget categories after signup
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)  # Authenticate user
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('home')  # Redirect to 'home' after successful login
            else:
                # Handle invalid credentials
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to home page after logout

def initial_setup_view(request):
    if request.method == 'POST':
        print("Received POST request")
        print("POST data:", request.POST)
        form = BudgetCategoryForm(request.POST)
        if form.is_valid():
            print("form valid!")
            form.save()
            print("redirecting now!")
            return redirect('home')  # Redirect to dashboard after adding a budget category
        else:
            print('errors')
            print(form.errors)
        
    else:
        form = BudgetCategoryForm(user=request.user)
    print("render form")
    return render(request, 'initial_setup.html', {'form': form})
