from django.urls import path
from users import views

app_name = 'users' 

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('verify-email/', views.verify_email_view, name='verify-email'),
]
