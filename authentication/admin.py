from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Customer)
admin.site.register(DeliveryGuy)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(DeliveryAddress)
admin.site.register(Delivery)
admin.site.register(Banner)