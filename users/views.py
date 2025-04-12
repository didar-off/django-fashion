from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from users.forms import RegistrationForm
from django.contrib.auth import login
from django.utils.translation import gettext_lazy as _
from users.utils import send_email_verification_code
from users.forms import RegistrationForm, VerificationCodeForm
from users.models import EmailVerificationCode, User
import logging


logger = logging.getLogger(__name__)

def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, _("You are already logged in."))
        return redirect("core:index")

    if request.method == "POST":
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                
                try:
                    send_email_verification_code(user, request)
                except Exception as e:
                    logger.error(f"Email sending failed: {str(e)}")
                    messages.error(request, _("Failed to send verification email. Please try again."))
                    return redirect('users:sign-up')

                request.session['verify_user_id'] = user.id
                return redirect('users:verify-email')
            
            except Exception as e:
                logger.error(f"Registration error: {str(e)}")
                messages.error(request, _("Registration failed. Please try again."))
                return redirect('users:sign-up')
    else:
        form = RegistrationForm()
    
    return render(request, "users/sign-up.html", {"form": form})


def verify_email_view(request):
    user_id = request.session.get("verify_user_id")
    if not user_id:
        messages.error(request, _("Session expired. Please register again."))
        return redirect("users:sign-up")
    
    user = get_object_or_404(User, id=user_id, is_active=False)

    if request.method == "POST":
        form = VerificationCodeForm(request.POST)
        if form.is_valid():
            code_input = form.cleaned_data["code"]
            try:
                code_obj = EmailVerificationCode.objects.filter(
                    user=user, 
                    is_used=False
                ).latest("created_at")
                
                if code_obj.is_expired():
                    messages.error(request, _("Code expired. Please register again."))
                    return redirect("users:sign-up")
                
                if code_obj.code == code_input:
                    user.is_active = True
                    user.save()
                    code_obj.is_used = True
                    code_obj.save()
                    login(request, user)
                    messages.success(request, _("Account verified!"))
                    return redirect("core:index")
                else:
                    messages.error(request, _("Invalid code"))
            except EmailVerificationCode.DoesNotExist:
                messages.error(request, _("No code found"))
    else:
        form = VerificationCodeForm()

    return render(request, "users/verify_email.html", {"form": form})


def login_view(request):
    return render(request, 'users/sign-in.html')