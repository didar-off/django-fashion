from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from users.forms import RegistrationForm, LoginForm


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('index')
        else:
            messages.error(request, "Please try again!")
    else:
        form = RegistrationForm()
    return render(request, 'users/sign-up.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('index')
        else:
            messages.error(request, "Invalid email or username!")
    else:
        form = LoginForm()
    return render(request, 'users/sign-in.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect('users:sign-in')
