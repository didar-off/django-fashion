from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from users.forms import RegistrationForm, VerificationCodeForm, LoginForm
from users.models import EmailVerificationCode, User
from users.utils import send_email_verification_code
import logging
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import timedelta

logger = logging.getLogger(__name__)

@require_http_methods(["GET", "POST"])
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
                send_email_verification_code(user, request)
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


def resend_code_view(request):
    user_id = request.session.get("verify_user_id")
    if not user_id:
        messages.error(request, _("Session expired. Please register again."))
        return redirect("users:sign-up")

    user = get_object_or_404(User, id=user_id, is_active=False)

    last_code = EmailVerificationCode.objects.filter(user=user).order_by('-created_at').first()
    if last_code and timezone.now() < last_code.created_at + timedelta(seconds=60):
        seconds_left = (last_code.created_at + timedelta(seconds=60) - timezone.now()).seconds
        messages.warning(request, _(f"Please wait {seconds_left} seconds before resending the code."))
        return redirect("users:verify-email")

    try:
        send_email_verification_code(user, request)
        messages.success(request, _("Verification code resent successfully."))
    except Exception as e:
        logger.error(f"Error resending code: {str(e)}")
        messages.error(request, _("Failed to resend verification code."))

    return redirect("users:verify-email")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("core:index")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if not request.POST.get("remember_me"):
                request.session.set_expiry(0)

            messages.success(request, _("Logged in successfully."))
            return redirect("core:index")
        else:
            messages.error(request, _("Invalid login credentials."))
    else:
        form = LoginForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, _("You have been logged out."))
    return redirect("users:login")
