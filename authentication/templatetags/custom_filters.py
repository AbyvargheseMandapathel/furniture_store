from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()

@register.filter
def mul(value, arg):
    """Multiply value by arg using Decimal."""
    try:
        return Decimal(value) * Decimal(arg)
    except (ValueError, TypeError, InvalidOperation):
        return Decimal("0")  # Return 0 if invalid input

@register.filter
def div(value, arg):
    """Divide value by arg using Decimal (avoiding division by zero)."""
    try:
        return Decimal(value) / Decimal(arg) if Decimal(arg) != 0 else Decimal("0")
    except (ValueError, TypeError, InvalidOperation):
        return Decimal("0")

@register.filter
def sub(value, arg):
    """Subtract arg from value using Decimal."""
    try:
        return Decimal(value) - Decimal(arg)
    except (ValueError, TypeError, InvalidOperation):
        return Decimal("0")
    
    
@register.filter
def get_range(value):
    return range(value)
