from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate,logout,get_user_model
from django.contrib import messages

from authentication.forms import BannerForm, CategoryForm, ComplaintForm, OrderTrackingForm, ProductForm, PromotionForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.db.models import Sum, Count
from django.db.models import Q

User = get_user_model()

# Signup View
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        role = request.POST.get("role")
        

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("signup")

        user = CustomUser.objects.create_user(username=username, email=email, password=password, role=role,first_name=first_name, last_name=last_name)

        if role == "customer":
            address = request.POST.get("customer_address")
            phone_number = request.POST.get("customer_number")
            print(phone_number)
            Customer.objects.create(user=user, address=address, phone_number=phone_number)

        elif role == "seller":
            store_name = request.POST.get("store_name")
            gst_number = request.POST.get("gst_number")
            phone_number = request.POST.get("seller_contact")
            print(phone_number)
            address = request.POST.get("address")
            Seller.objects.create(user=user, store_name=store_name, gst_number=gst_number,phone_number=phone_number,address=address)

        elif role == "delivery_guy":
            vehicle_number = request.POST.get("vehicle_number")
            phone_number = request.POST.get("phone_number")
            print(phone_number)
            DeliveryGuy.objects.create(user=user, vehicle_number=vehicle_number, availability_status=True,phone_number=phone_number)

        login(request, user)
        messages.success(request, "Signup successful!")

        # **Redirect based on role**
        return redirect(dashboard)

    return render(request, "signup.html")

# Login View


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        if not username or not password:
            messages.error(request, "Both username and password are required!")
            return redirect("login")  # Redirect back to login page

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful! ")
            return redirect("dashboard")  # Ensure this URL exists
        else:
            messages.error(request, "Invalid username or password!")
            return redirect("login")  # Redirect back to login page

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
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(total_revenue=models.Sum('total_price'))['total_revenue'] or 0
    total_products = Product.objects.count()

    orders_list = Order.objects.select_related('customer').order_by('-ordered_at')
    paginator = Paginator(orders_list, 5)  # Show 5 orders per page

    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'total_products': total_products,
        'orders': orders,  # Pass paginated orders
    }
    return render(request, 'admin_dashboard.html', context)


@user_passes_test(is_seller)
def seller_dashboard(request):
    total_sales = Order.objects.aggregate(total=Sum("total_price"))["total"] or 0
    total_orders = Order.objects.count()
    top_products = Product.objects.annotate(sales=Sum("orders__quantity")).order_by("-sales")[:5]
    
    total_revenue = sum(product.price * product.sales for product in top_products)

    context = {
        "total_sales": total_sales,
        "total_orders": total_orders,
        "top_products": top_products,
        "total_revenue": total_revenue,
    }
    
    return render(request, "seller_dashboard.html", context)

@user_passes_test(is_delivery)
def delivery_dashboard(request):
    return render(request, "delivery_dashboard.html")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def seller_list(request):
    sellers = Seller.objects.all()
    
    # Get filter parameters from GET request
    store_name = request.GET.get('store_name', '').strip()
    phone_number = request.GET.get('phone_number', '').strip()
    approval_status = request.GET.get('approval_status', '')

    # Apply filters
    if store_name:
        sellers = sellers.filter(store_name__icontains=store_name)
    if phone_number:
        sellers = sellers.filter(phone_number__icontains=phone_number)
    if approval_status:
        if approval_status == 'approved':
            sellers = sellers.filter(is_approved=True)
        elif approval_status == 'pending':
            sellers = sellers.filter(is_approved=False)

    return render(request, 'sellers.html', {
        'sellers': sellers,
        'store_name': store_name,
        'phone_number': phone_number,
        'approval_status': approval_status
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delivery_list(request):
    delivery_agents = DeliveryGuy.objects.all()
    
    # Get filter parameters from GET request
    name = request.GET.get('name', '').strip()
    phone_number = request.GET.get('phone_number', '').strip()
    approval_status = request.GET.get('approval_status', '')

    # Apply filters
    if name:
        delivery_agents = delivery_agents.filter(name__icontains=name)
    if phone_number:
        delivery_agents = delivery_agents.filter(phone_number__icontains=phone_number)
    if approval_status:
        if approval_status == 'approved':
            delivery_agents = delivery_agents.filter(is_approved=True)
        elif approval_status == 'pending':
            delivery_agents = delivery_agents.filter(is_approved=False)

    return render(request, 'delivery_agents.html', {
        'delivery_agents': delivery_agents,
        'name': name,
        'phone_number': phone_number,
        'approval_status': approval_status
    })


@login_required
@user_passes_test(lambda u: u.is_superuser)  # Only allow superusers
def update_approval_status(request, user_id, role, action):
    if role == 'seller':
        user_instance = get_object_or_404(Seller, user_id=user_id)
    elif role == 'delivery_guy':
        user_instance = get_object_or_404(DeliveryGuy, user_id=user_id)
    else:
        messages.error(request, "Invalid role.")
        return redirect('dashboard')

    if action == 'approve':
        user_instance.is_approved = True
        messages.success(request, f"{role.replace('_', ' ').title()} approved successfully.")
    elif action == 'suspend':
        user_instance.is_approved = False
        messages.warning(request, f"{role.replace('_', ' ').title()} suspended.")
    elif action == 'reject':
        user_instance.user.delete()  # Delete user and seller record
        messages.error(request, f"{role.replace('_', ' ').title()} rejected and removed.")
        return redirect('dashboard')  # Redirect early to avoid saving

    user_instance.save()
    return redirect('dashboard')  # Redirect to admin dashboard



@login_required
def product_list(request):
    if request.user.is_superuser:  
        products = Product.objects.all()
    else:  
        products = Product.objects.filter(created_by=request.user.seller)
    
    return render(request, "product_list.html", {"products": products})

@login_required
def approve_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.is_approved = True
    product.save()
    return redirect("product_list")

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect("product_list")

@login_required
def manage_categories(request):
    categories = Category.objects.all()
    return render(request, "manage_categories.html", {"categories": categories})

@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect("manage_categories")
        else:
            messages.error(request, "Failed to add category. Please check the form.")
    else:
        form = CategoryForm()
    return render(request, "add_category.html", {"form": form})

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, "Category deleted successfully.")
    return redirect("manage_categories")


@login_required
def manage_content(request):
    banners = Banner.objects.all()
    promotions = Promotion.objects.all()
    return render(request, "manage_content.html", {"banners": banners, "promotions": promotions})

@login_required
def add_banner(request):
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Banner added successfully.")
            return redirect("manage_content")
    else:
        form = BannerForm()
    return render(request, "add_edit_content.html", {"form": form, "title": "Add Banner"})

@login_required
def delete_banner(request, banner_id):
    banner = get_object_or_404(Banner, id=banner_id)
    banner.delete()
    messages.success(request, "Banner deleted successfully.")
    return redirect("manage_content")

@login_required
def add_promotion(request):
    if request.method == "POST":
        form = PromotionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Promotion added successfully.")
            return redirect("manage_content")
    else:
        form = PromotionForm()
    return render(request, "add_edit_content.html", {"form": form, "title": "Add Promotion"})

@login_required
def delete_promotion(request, promotion_id):
    promotion = get_object_or_404(Promotion, id=promotion_id)
    promotion.delete()
    messages.success(request, "Promotion deleted successfully.")
    return redirect("manage_content")



def track_order(request):
    form = OrderTrackingForm()
    order_info = None

    if request.method == "POST":
        form = OrderTrackingForm(request.POST)
        if form.is_valid():
            order_id = form.cleaned_data["order_id"]
            order_info = get_object_or_404(Order, order_id=order_id)

    return render(request, "track_order.html", {"form": form, "order_info": order_info})

# ✅ Delivery Tracking View
def track_delivery(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    delivery = Delivery.objects.filter(order=order).first()
    return render(request, "track_delivery.html", {"order": order, "delivery": delivery})

# ✅ Complaint Submission View
def submit_complaint(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your complaint has been submitted.")
            return redirect("submit_complaint")
    else:
        form = ComplaintForm()

    return render(request, "submit_complaint.html", {"form": form})


@login_required
def view_complaints(request):
    if request.user.is_superuser:  # Admin
        complaints = Complaint.objects.all()
    elif hasattr(request.user, 'seller'):  # Seller
        complaints = Complaint.objects.filter(order__seller=request.user.seller)
    else:
        complaints = Complaint.objects.none()  # Unauthorized users get no complaints

    return render(request, "view_complaints.html", {"complaints": complaints})


@login_required
def track_orders(request):
    user = request.user
    print(f"User: {user}, Role: {getattr(user, 'role', 'No role')}")

    if user.role == "admin":
        orders = Order.objects.select_related("customer", "product", "delivery").order_by("-ordered_at")
    elif hasattr(user, "seller"):  # If user is a seller
        print("User is a seller")
        orders = Order.objects.filter(product__seller=user.seller).select_related("customer", "product", "delivery").order_by("-ordered_at")
    elif hasattr(user, "customer"):  # If user is a customer
        print("User is a customer")
        orders = Order.objects.filter(customer=user.customer).select_related("product", "delivery").order_by("-ordered_at")
    elif hasattr(user, "delivery_guy"):  # If user is a delivery guy
        print("User is a delivery guy")
        orders = Order.objects.filter(delivery=user.delivery_guy).select_related("customer", "product").order_by("-ordered_at")
    else:
        print("User has no role")
        orders = Order.objects.none()  # Empty queryset if user has no role

    print(f"Orders found: {orders.count()}")

    # Paginate the orders (5 per page)
    paginator = Paginator(orders, 5)
    page_number = request.GET.get("page")
    orders_page = paginator.get_page(page_number)

    return render(request, "track_orders.html", {"orders": orders_page})
@login_required
def track_orders(request):
    user = request.user

    if user.role == "admin":
        orders = Order.objects.select_related("customer__user", "product", "seller").order_by("-ordered_at")
    elif hasattr(user, "seller"):  # If user is a seller
        print(user.seller)
        orders = Order.objects.filter(seller=request.user.seller).order_by("-ordered_at")
        print(orders)
    elif hasattr(user, "customer"):  # If user is a customer
        orders = Order.objects.filter(customer=user.customer).select_related("product", "seller").order_by("-ordered_at")
    else:
        orders = Order.objects.none()  # Empty queryset if user has no role

    # Paginate the orders (5 per page)
    paginator = Paginator(orders, 5)
    page_number = request.GET.get("page")
    orders_page = paginator.get_page(page_number)

    return render(request, "track_orders.html", {"orders": orders_page})


@login_required
def add_product(request):
    try:
        seller = Seller.objects.get(user=request.user)  # Ensure user has a seller profile
    except Seller.DoesNotExist:
        messages.error(request, "Only approved sellers can add products.")
        return redirect("home")

    if not seller.is_approved:  # Ensure seller is approved
        messages.error(request, "Your seller account is not approved yet.")
        return redirect("login")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = seller  # Assign seller as created_by
            product.save()
            messages.success(request, "Product added successfully! Waiting for admin approval.")
            return redirect("product_list")

    else:
        form = ProductForm()

    return render(request, "add_product.html", {"form": form})
# Order Management
@login_required
def order_list(request):
    if request.user.role == "seller":
        orders = Order.objects.filter(product__created_by=request.user.seller)
    else:
        orders = Order.objects.filter(user=request.user)
    return render(request, "order_list.html", {"orders": orders})

@login_required
def update_order_status(request, order_id, status):
    order = get_object_or_404(Order, id=order_id)
    order.status = status
    order.save()
    messages.success(request, f"Order status updated to {status}.")
    return redirect("order_list")


@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        seller = Seller.objects.get(user=request.user)  # Get logged-in seller
    except Seller.DoesNotExist:
        messages.error(request, "Only approved sellers can update products.")
        return redirect("home")

    if product.created_by != seller:
        messages.error(request, "You are not authorized to update this product.")
        return redirect("product_list")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)

    return render(request, "update_product.html", {"form": form, "product": product})


def customer_list(request):
    query = request.GET.get("q", "")
    category = request.GET.get("category", "")
    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category:
        products = products.filter(category__name=category)

    paginator = Paginator(products, 10)  # 10 products per page
    page_number = request.GET.get("page")
    products_page = paginator.get_page(page_number)

    return render(request, "products.html", {"products": products_page})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})


# 🚀 Cart Views
def cart_view(request):
    cart = Cart.objects.filter(user=request.user.customer)
    return render(request, "cart.html", {"cart": cart})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    user = User.objects.get(username="customertwo")  # Replace with actual username
    customer = Customer.objects.get(user=user)  # This should return a valid Customer instance
    print(customer)

    # Ensure request.user is a Customer instance
    try:
        customer = Customer.objects.get(user=request.user.customer)
    except Customer.DoesNotExist:
        messages.error(request, "Only customers can add products to the cart.")
        return redirect("product_list")  # Redirect to products page or any relevant page

    # Get or create a cart item
    cart_item, created = Cart.objects.get_or_create(user=customer, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Added to cart!")
    return redirect("cart")


def remove_from_cart(request, pk):
    cart_item = get_object_or_404(Cart, user=request.user.customer, product_id=pk)
    cart_item.delete()
    messages.success(request, "Removed from cart!")
    return redirect("cart")


# 🚀 Checkout View
def checkout(request):
    customer = request.user.customer
    cart = Cart.objects.filter(user=customer)

    if not cart.exists():
        messages.error(request, "Your cart is empty!")
        return redirect("product_list")

    total_price = sum(item.product.price * item.quantity for item in cart)

    for item in cart:
        order = Order.objects.create(
            customer=customer,
            product=item.product,
            seller=item.product.created_by,  # Ensure `product` has a `seller` field
            quantity=item.quantity,
            total_price=item.product.price * item.quantity,
        )
        item.delete()  # Remove item from cart after ordering

    messages.success(request, "Order placed successfully!")
    return redirect("customer_list")


# 🚀 Coupon Application
def apply_coupon(request):
    code = request.GET.get("code", "")
    coupon = Coupon.objects.filter(code=code, is_active=True).first()

    if not coupon:
        messages.error(request, "Invalid or expired coupon!")
        return redirect("cart")

    request.session["discount"] = coupon.discount_percentage
    messages.success(request, f"Coupon applied! {coupon.discount_percentage}% off.")
    return redirect("cart")


def home(request):
    return render(request, "home.html")