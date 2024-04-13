from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST,user=request.user)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  # Redirect to home page after successful signup
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
                return redirect('dashboard')  # Redirect to 'home' after successful login
            else:
                # Handle invalid credentials
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to home page after logout
