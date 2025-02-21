from django import forms
from .models import Complaint, Product, Category,Banner,Promotion,Order

from .models import DeliveryAddress

from django import forms
from .models import DeliveryAddress

class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ["full_name", "address", "city", "zipcode", "country"]
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'Enter your full name',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'Enter your address',
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'Enter your city',
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'Enter your zipcode',
            }),
            'country': forms.TextInput(attrs={
                'class': 'form-input w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500',
                'placeholder': 'Enter your country',
            }),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "description", "price", "image"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "Product Name"
            }),
            "category": forms.Select(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "rows": 4,
                "placeholder": "Detailed product description..."
            }),
            "price": forms.NumberInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "0.00",
                "step": "0.01"
            }),
            "image": forms.FileInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100"
            }),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500",
                "placeholder": "New category name"
            }),
        }
        
class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ["title", "image", "link", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full border-gray-300 rounded-lg shadow-sm"}),
            "image": forms.ClearableFileInput(attrs={"class": "w-full border-gray-300 rounded-lg shadow-sm"}),
            "link": forms.URLInput(attrs={"class": "w-full border-gray-300 rounded-lg shadow-sm"}),
            "is_active": forms.CheckboxInput(attrs={"class": "rounded text-blue-600"}),
        }

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ["title", "description", "image", "link", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "w-full border-gray-300 rounded-lg shadow-sm"}),
            "description": forms.Textarea(attrs={"class": "w-full border-gray-300 rounded-lg shadow-sm", "rows": 3}),
            "image": forms.ClearableFileInput(attrs={"class": "w-full border-gray-300 rounded-lg shadow-sm"}),
            "link": forms.URLInput(attrs={"class": "w-full border-gray-300 rounded-lg shadow-sm"}),
            "is_active": forms.CheckboxInput(attrs={"class": "rounded text-blue-600"}),
        }
        
        
class OrderTrackingForm(forms.Form):
    order_id = forms.UUIDField(
        label="Enter Order ID",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'e.g. 123e4567-e89b-12d3-a456-426614174000',
            'pattern': '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
        })
    )

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ["order", "message"]
        widgets = {
            "order": forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'data-placeholder': 'Select your order'
            }),
            "message": forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Please describe your issue in detail...'
            }),
        }
        
        
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "image", "category", "price", "description", "stock"]
        widgets = {
            "name": forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Product Name'
            }),
            "image": forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            }),
            "category": forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            "price": forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': '0.00',
                'step': '0.01'
            }),
            "description": forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 4,
                'placeholder': 'Product description...'
            }),
            "stock": forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Available stock'
            }),
        }