from django.urls import reverse
from django.shortcuts import redirect

def base_template_processor(request):
    # Default base template
    base_template = None

    # Ensure user is authenticated
    if request.user.is_authenticated:
        user_role = request.user.role  

        # Mapping user roles to base templates
        base_templates = {
            "admin": "base/admin_base.html",
            "customer": "base/customer_base.html",
            "seller": "base/seller_base.html",
            "delivery_guy": "base/delivery_base.html",
        }

        # Get the base template if the role exists
        base_template = base_templates.get(user_role, base_template)

    return {"base_template": base_template}
