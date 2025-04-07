from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from users.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'full_name', 'user_type', 'image', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email")
