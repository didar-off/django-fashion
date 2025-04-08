# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from users.models import User

# class RegistrationForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ('email', 'full_name', 'user_type', 'password1', 'password2', 'image')

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['user_type'].choices = [
#             ('customer', 'Customer'),
#             ('vendor', 'Vendor'),
#         ]

# class LoginForm(AuthenticationForm):
#     username = forms.EmailField(label="Email")
