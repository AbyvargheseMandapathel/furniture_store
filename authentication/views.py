from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout,get_user_model
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

User = get_user_model()

# Signup View
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("signup")

        user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role)

        if role == "customer":
            address = request.POST.get("address")
            phone_number = request.POST.get("phone_number")
            Customer.objects.create(user=user, address=address, phone_number=phone_number)

        elif role == "seller":
            store_name = request.POST.get("store_name")
            gst_number = request.POST.get("gst_number")
            Seller.objects.create(user=user, store_name=store_name, gst_number=gst_number)

        elif role == "delivery_guy":
            vehicle_number = request.POST.get("vehicle_number")
            DeliveryGuy.objects.create(user=user, vehicle_number=vehicle_number, availability_status=True)

        login(request, user)
        messages.success(request, "Signup successful!")

        # **Redirect based on role**
        return redirect(dashboard)

    return render(request, "signup.html")

# Login View


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(f"Username: {username}")
        print(f"Password: {password}")

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        print(f"Authenticated User: {user}")

        if user is not None:
            login(request, user)
            print("User logged in successfully!")
            return redirect("dashboard")  # Ensure 'dashboard' URL is properly defined in urls.py
        else:
            print("Invalid credentials!")
            return render(request, "login.html", {"error": "Invalid username or password!"})

    return render(request, "login.html")

# Logout View
@login_required
def user_logout(request):
    logout(request)
    return redirect("login")

# Dashboard View (Role-Based Redirect)
@login_required
def dashboard(request):
    user  = request.user
    print(user.role)
    if user.role == "admin":
        return redirect("admin_dashboard")
    elif request.user.role == "customer":
        return redirect("customer_dashboard")
    elif request.user.role == "delivery_guy":
        return redirect("delivery_dashboard")
    elif request.user.role == "seller":
        return redirect("seller_dashboard")
    return redirect("login")


def is_admin(user):
    return user.role in ['admin']


def is_delivery(user):
    return user.role in ['delivery_guy']

def is_seller(user):
    return user.role in ['seller']

def is_customer(user):
    return user.role in ['customer']
# def is_admin_or_teacher(user):
#     return user.user_type in ['admin', 'teacher']


@user_passes_test(is_customer)
def customer_dashboard(request):
    return render(request, "customer_dashboard.html")


@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, "admin_dashboard.html")


@user_passes_test(is_seller)
def seller_dashboard(request):
    return render(request, "seller_dashboard.html")

@user_passes_test(is_delivery)
def delivery_dashboard(request):
    return render(request, "delivery_dashboard.html")