from django.urls import path
from users import views

app_name = 'users' 

urlpatterns = [
    path('sign-up/', views.register_view, name='sign-up'),
    path('sign-in/', views.login_view, name='login'),
    # path('sign-out/', views.logout_view, name='logout'),
]
