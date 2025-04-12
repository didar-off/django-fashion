from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from users.models import User


class RegistrationForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=100,
        label='Full Name',
        widget=forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': 'form-control'})
    )
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        label='User Type',
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        initial='customer'
    )
    image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'full_name', 'user_type', 'image', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.full_name = self.cleaned_data['full_name']
        user.user_type = self.cleaned_data['user_type']
        image = self.cleaned_data.get('image')
        if image:
            user.image = image
        if commit:
            user.save()
        return user


class VerificationCodeForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        label="Enter the 6-digit code",
        widget=forms.TextInput(attrs={"placeholder": "123456"})
    )