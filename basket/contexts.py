from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.conf import settings

from products.models import Product


def calculate_delivery(total):
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0
    return delivery, free_delivery_delta


def get_basket_items(basket):
    items = []
    total = 0
    product_count = 0

    for item_id, quantity in basket.items():
        product = get_object_or_404(Product, pk=item_id)
        total += quantity * product.price
        product_count += quantity
        items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })

    return items, total, product_count


def basket_contents(request):
    basket = request.session.get('basket', {})
    basket_items, total, product_count = get_basket_items(basket)
    delivery, free_delivery_delta = calculate_delivery(total)
    grand_total = delivery + total

    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
