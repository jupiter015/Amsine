from django.contrib import admin
from django.urls import path, include
from . import views

app_name = "RegisterPage"

urlpatterns = [
    path('', views.index, name='index'),
    path('verify/', views.email_verification_page, name="email_verification_page"),
    path('verify/checkAuthCode', views.check_auth_code, name='checkAuthCode'),
    path('usernameCheck/', views.usernameCheck, name='usernameCheck'),
    path('checkEmailUser/', views.checkEmailUsed, name='checkEmailUsed'),
    path('registerButton/', views.registerButton, name='registerButton')
]