from django.contrib import admin
from .models import CustomUser, Customer, Seller, DeliveryGuy

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(DeliveryGuy)
admin.site.register(Seller)