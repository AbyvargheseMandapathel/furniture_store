from django.urls import path
from .views import *

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('customer-dashboard/', customer_dashboard, name='customer_dashboard'),
    path('delivery-dashboard/', delivery_dashboard, name='delivery_dashboard'),
    path('seller-dashboard/', seller_dashboard, name='seller_dashboard'),
]
