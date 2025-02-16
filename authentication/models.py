import uuid
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("customer", "Customer"),
        ("seller", "Seller"),
        ("delivery_guy", "Delivery Guy"),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")

    # Fix conflicts by setting related_name
    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:  # Ensure superuser is always an admin
            self.role = "admin"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"


# ✅ Separate classes for different user types
class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField()
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return f"Customer: {self.user.username}"


class Seller(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    store_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=15, unique=True)
    phone_number = models.CharField(max_length=15)
    address = models.TextField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Seller: {self.store_name}"


class DeliveryGuy(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    vehicle_number = models.CharField(max_length=20)
    availability_status = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Delivery Guy: {self.user.username}"


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    created_by = models.ForeignKey(Seller, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="products/")
    is_approved = models.BooleanField(default=False)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
    
class Banner(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to="banners/")
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Promotion(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="promotions/")
    link = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    
class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
        ("returned", "Returned"),
    ]

    PAYMENT_METHODS = [
        ("cod", "Cash on Delivery"),
    ]

    order_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orders")
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, related_name="orders_seller")
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default="cod")
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.customer.username}"

class Delivery(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery")
    delivery_guy = models.ForeignKey(DeliveryGuy, on_delete=models.SET_NULL, null=True, blank=True)
    estimated_delivery = models.DateTimeField()
    delivered_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[("out_for_delivery", "Out for Delivery"), ("delivered", "Delivered"), ("failed", "Failed")],
        default="out_for_delivery",
    )

    def __str__(self):
        return f"Delivery for Order {self.order.order_id}"

class Complaint(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="complaints")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    complaint_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return f"Complaint for Order {self.order.order_id}"
    
class Cart(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.user.username})"
    
    
class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Discount in %
    gives_free_premium = models.BooleanField(default=False)  # Does it give free premium access?
    expires_at = models.DateTimeField()  # Expiration date
    usage_limit = models.PositiveIntegerField(default=1)  # How many times it can be used
    used_count = models.PositiveIntegerField(default=0)  # Track usage count
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        """Check if the coupon is valid (not expired & usage limit not reached)."""
        return self.expires_at > timezone.now() and self.used_count < self.usage_limit

    def use_coupon(self):
        """Mark the coupon as used (if valid)."""
        if self.is_valid():
            self.used_count += 1
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}% (Used: {self.used_count}/{self.usage_limit})"