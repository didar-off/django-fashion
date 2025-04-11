from django.contrib import messages
from django.shortcuts import render, redirect
from users.forms import RegistrationForm
from users.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Your account has been created successfully.")
            return redirect('store:index')
    else:
        form = RegistrationForm()
    return render(request, 'users/sign-up.html', {'form': form})


def login_view(request):
    return render(request, 'users/sign-in.html')