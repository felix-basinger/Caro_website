from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('account/', views.account, name='account'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
    path('password-reset/', views.password_reset_request, name='password_reset_request'),
    path('password-reset/code/', views.password_reset_code, name='password_reset_code'),
    path('password-reset/set-new-password/<int:user_id>/', views.set_new_password, name='set_new_password'),
    path('resend-reset-code/', views.resend_reset_code, name='resend_reset_code'),
]
