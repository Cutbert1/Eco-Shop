from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

from products.models import Product
import logging

logger = logging.getLogger(__name__)
# Create your views here.


def view_basket(request):
    """ Renders current content of user shopping backet.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered basket page.
    """

    return render(request, 'basket/basket.html')


def add_item_to_basket(request, item_id):
    """Add a specific quantity of an item to the shopping basket.

    Args:
        request (HttpRequest): HTTP request object that contains
            the POST data with 'quantity' and optional 'redirect_url'.
        item_id (int or str): ID of the product to add.

        Returns:
        HttpResponseRedirect: Redirects URL.
    """

    product = Product.objects.get(pk=item_id)

    quantity = get_quantity_from_request(request)
    redirect_url = request.POST.get('redirect_url')
    basket = get_basket_from_session(request)

    update_basket(basket, item_id, quantity)

    request.session['basket'] = basket
    messages.success(request, f'Added {product.name} to your basket')
    return redirect(redirect_url)


def get_quantity_from_request(request):
    return int(request.POST.get('quantity', 1))


def get_basket_from_session(request):
    return request.session.get('basket', {})


def update_basket(basket, item_id, quantity):
    basket[item_id] = basket.get(item_id, 0) + quantity


def update_basket_quantity(request, item_id):
    """ Update quantity of individual product in a user's basket
        If quantity is set to zero or less, the item is removed.

    Args:
        request (HttpRequest): HTTP request object which has
            the new quantity in POST data.
        item_id (str or int): ID of the product to update.

    Returns:
        HttpResponseRedirect: Redirects to the basket view page.
    """

    product = Product.objects.get(pk=item_id)

    quantity = int(request.POST.get('quantity', 0))
    basket = request.session.get('basket', {})

    if quantity > 0:
        basket[item_id] = quantity
    else:
        basket.pop(item_id, None)

    request.session['basket'] = basket
    messages.success(request, f'{product.name} : quantity updated to {basket[item_id]}')  # noqa
    return redirect(reverse('view_basket'))


@require_POST
def remove_from_basket(request, item_id):
    """ Remove a specific product from the
        shopping basket through AJAX request.

    Args:
        request (HttpRequest): HTTP request object.
        item_id (str or int): ID of the product to be removed.

    Returns:
        JsonResponse: JSON response indicating success or error.
    """

    product = Product.objects.get(pk=item_id)

    try:
        basket = request.session.get('basket', {})

        if not item_id:
            return JsonResponse({'error': 'Item ID is required'}, status=400)

        if item_id in basket:
            basket.pop(item_id)
            request.session['basket'] = basket
            messages.success(request, f'Removed {product.name} from basket')
            return JsonResponse({
                'message': 'Item removed successfully'
                }, status=200)
        else:
            return JsonResponse({
                'error': 'Item not found in basket'}, status=404
                )

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return JsonResponse({
            'error': 'An error occurred while removing the item'
            }, status=500)
