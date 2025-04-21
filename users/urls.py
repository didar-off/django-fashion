from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from users import views

app_name = 'users' 

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('verify-email/', views.verify_email_view, name='verify-email'),
    path('resend-code/', views.resend_code_view, name='resend-code'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Password reset URLs
    path('forgot-password/', auth_views.PasswordResetView.as_view(
        template_name='users/forgot_password.html',
        email_template_name='users/password_reset_email.html',
        subject_template_name='users/password_reset_subject.txt',
        success_url=reverse_lazy('users:password_reset_done')
    ), name='password_reset'),

    path('forgot-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'
    ), name='password_reset_complete'),
]
