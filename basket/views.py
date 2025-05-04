from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import logging

logger = logging.getLogger(__name__)
# Create your views here.


def view_basket(request):
    """ Renders content of backet page"""

    return render(request, 'basket/basket.html')


def add_item_to_basket(request, item_id):
    """Add a specific quantity of an item to the shopping basket."""

    quantity = get_quantity_from_request(request)
    redirect_url = request.POST.get('redirect_url')
    basket = get_basket_from_session(request)

    update_basket(basket, item_id, quantity)

    request.session['basket'] = basket
    return redirect(redirect_url)


def get_quantity_from_request(request):
    return int(request.POST.get('quantity', 1))


def get_basket_from_session(request):
    return request.session.get('basket', {})


def update_basket(basket, item_id, quantity):
    basket[item_id] = basket.get(item_id, 0) + quantity


def update_basket_quantity(request, item_id):
    """ Update quantity of individual product in a user's basket """

    quantity = int(request.POST.get('quantity', 0))
    basket = request.session.get('basket', {})

    if quantity > 0:
        basket[item_id] = quantity
    else:
        basket.pop(item_id, None)

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))


@require_POST
def remove_from_basket(request, item_id):
    """ Remove the item from the shopping basket """
    try:
        basket = request.session.get('basket', {})

        if not item_id:
            return JsonResponse({'error': 'Item ID is required'}, status=400)

        if item_id in basket:
            basket.pop(item_id)
            request.session['basket'] = basket
            return JsonResponse({
                'message': 'Item removed successfully'
                }, status=200)
        else:
            return JsonResponse({
                'error': 'Item not found in basket'}, status=404
                )

    except Exception as e: ## noqa
        return JsonResponse({
            'error': 'An error occurred while removing the item'
            }, status=500)
