from django.shortcuts import render, redirect

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
