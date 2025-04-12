from django.core.mail import get_connection, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from users.models import EmailVerificationCode
import logging


logger = logging.getLogger(__name__)

def send_email_verification_code(user, request=None):
    try:
        from .models import EmailVerificationCode
        
        code = EmailVerificationCode.generate_code()
        EmailVerificationCode.objects.create(user=user, code=code)

        subject = "Your verification code"
        message = render_to_string("users/verification_code_email.html", {
            "user": user,
            "code": code,
        })

        with get_connection(
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS
        ) as connection:
            email = EmailMessage(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                connection=connection,
            )
            email.send()

    except Exception as e:
        logger.error(f"Error sending verification email: {str(e)}")
        raise