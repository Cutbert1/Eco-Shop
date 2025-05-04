from django import template
from decimal import Decimal, InvalidOperation


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Calculate the subtotal of an item based on its price and quantity.

    Args:
        price (float or Decimal): The price of the item.
        quantity (int): The quantity of the item.

    Returns:
        Decimal: The calculated subtotal.
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
        value (float or Decimal): The value to format.

    Returns:
        str: The formatted currency string.
    """
    try:
        return f"${value:.2f}"
    except (ValueError, TypeError):
        return "$0.00"


@register.simple_tag
def calc_total(items):
    """
    Calculate the total sum of all items.

    Args:
        items (list): A list of dictionaries containing 'price' and 'quantity' keys.  # noqa

    Returns:
        Decimal: The calculated total.
    """
    total = sum(calc_subtotal(
        item['price'], item['quantity']) for item in items
        )
    return total.quantize(Decimal('0.01'))
