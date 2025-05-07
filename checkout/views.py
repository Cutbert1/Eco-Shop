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
            'stripe_public_key': "pk_test_51RM3reISvKrbInR2EBqe5LzOs0JKZrxdvoxlAvLG0ZaAh7GAezJqgoR1cFits3ntI3Ood80Qnfu4dEvEXwrTxw54007H4avRe9",  # noqa
            'client_secret': 'test client secret',
        }
        return render(request, template, context)

    basket = get_basket(request)
    if not basket:
        display_empty_basket_message(request)
        return redirect(reverse('products'))

    order_form = OrderForm()
    return render_checkout_page(request, order_form)
