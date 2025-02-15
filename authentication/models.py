from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _

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

    def __str__(self):
        return f"Seller: {self.store_name}"


class DeliveryGuy(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    vehicle_number = models.CharField(max_length=20)
    availability_status = models.BooleanField(default=True)

    def __str__(self):
        return f"Delivery Guy: {self.user.username}"
