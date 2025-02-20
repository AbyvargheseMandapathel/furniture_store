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
    
    
    path('update-approval/<int:user_id>/<str:role>/<str:action>/', update_approval_status, name='update_approval_status'),
    path('sellers/', seller_list, name='seller_list'),
    path('delivery-agents/', delivery_list, name='delivery_list'),
    
    
    path("products/", product_list, name="product_list"),
    path("products/<int:product_id>/approve/", approve_product, name="approve_product"),
    path("products/<int:product_id>/delete/", delete_product, name="delete_product"),
    path("categories/", manage_categories, name="manage_categories"),
    path("categories/add/", add_category, name="add_category"),
    path("categories/delete/<int:category_id>/", delete_category, name="delete_category"),
    
    
    path("content-management/", manage_content, name="manage_content"),
    path("content-management/banner/add/", add_banner, name="add_banner"),
    path("content-management/banner/delete/<int:banner_id>/", delete_banner, name="delete_banner"),
    path("content-management/promotion/add/", add_promotion, name="add_promotion"),
    path("content-management/promotion/delete/<int:promotion_id>/", delete_promotion, name="delete_promotion"),
    
    path("track-order/", track_order, name="track_order"),
    path("track-delivery/<uuid:order_id>/", track_delivery, name="track_delivery"),
    path("submit-complaint/", submit_complaint, name="submit_complaint"),
    path("view-complaints/", view_complaints, name="view_complaints"),
    path("track-orders/", track_orders, name="track_orders"),
    
    path("add-product/", add_product, name="add_product"),
    path("orders/", order_list, name="order_list"),
    path("update-order/<int:order_id>/<str:status>/", update_order_status, name="update_order_status"),
    path("update-product/<int:product_id>/", update_product, name="update_product"),
    
    
    path("", customer_list, name="customer_list"),
    path("products/<int:pk>/", product_detail, name="product_detail"),

    # Cart & Checkout
    path("cart/", cart_view, name="cart"),
    path("cart/add/<int:pk>/", add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:pk>/", remove_from_cart, name="remove_from_cart"),
    path("checkout/", checkout, name="checkout"),

    # Coupons
    path("apply-coupon/", apply_coupon, name="apply_coupon"),
    path("update-order-status/", update_order_status, name="update_order_status"),
    
    # path("home/", home, name="home"),
    # path("delivery-addresses/add/<int:product_id>/", add_delivery_addresss, name="add_delivery_address"),]
    path("delivery-addresses/add/", add_delivery_address, name="add_delivery_address"),  
# path("delivery-addressesList", add_deliveryList, name="add_delivery_address"),  
]
