from django import template
from decimal import Decimal, InvalidOperation


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Calculate the subtotal of an item based on its price and quantity.

    Args:
        price (float or Decimal): Price of the item.
        quantity (int): Quantity of the item.

    Returns:
        Decimal: Calculated subtotal.
    """
    try:
        price = Decimal(price)
        quantity = int(quantity)
        return (price * quantity).quantize(Decimal('0.01'))
    except (ValueError, TypeError, InvalidOperation):
        return Decimal('0.00')


@register.filter(name='format_currency')
def format_currency(value):
    """
    Format a number as currency.

    Args:
        value (float or Decimal): Value to format.

    Returns:
        str: Formatted currency string.
    """
    try:
        return f"${value:.2f}"
    except (ValueError, TypeError):
        return "$0.00"


@register.simple_tag
def calc_total(items):
    """
    Calculate total sum of all items.

    Args:
        items (list): List of dictionaries containing 'price' and 'quantity' keys.  # noqa

    Returns:
        Decimal: Calculated total.
    """
    total = sum(calc_subtotal(
        item['price'], item['quantity']) for item in items
        )
    return total.quantize(Decimal('0.01'))
