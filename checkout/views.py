from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm

# Create your views here.


def checkout(request):
    def get_basket(request):
        return request.session.get('basket', {})

    def display_empty_basket_message(request):
        messages.error(request, "Your basket is currently empty")

    def render_checkout_page(request, order_form):
        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
        }
        return render(request, template, context)

    basket = get_basket(request)
    if not basket:
        display_empty_basket_message(request)
        return redirect(reverse('products'))

    order_form = OrderForm()
    return render_checkout_page(request, order_form)
