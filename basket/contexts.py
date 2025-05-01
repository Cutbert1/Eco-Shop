from decimal import Decimal
from django.conf import settings


def calculate_delivery(total):
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    return delivery, free_delivery_delta


def get_basket_context(basket_items, total, product_count):
    delivery, free_delivery_delta = calculate_delivery(total)
    grand_total = delivery + total

    return {
        'basket_items': basket_items,
        'product_count': product_count,
        'delivery': delivery,
        'total': total,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'free_delivery_delta': free_delivery_delta,
        'grand_total': grand_total,
    }


def basket_contents(request):
    basket_items = []
    total = 0
    product_count = 0

    return get_basket_context(basket_items, total, product_count)
