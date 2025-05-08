from django.shortcuts import render, redirect, reverse
from django.conf import settings
from django.contrib import messages
from .forms import OrderForm
from basket.contexts import basket_contents

import stripe

# Create your views here.


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    def get_basket(request):
        return request.session.get('basket', {})

    def show_empty_basket_message(request):
        messages.error(request, "Your basket is currently empty")

    def create_payment_intent(amount):
        stripe.api_key = stripe_secret_key
        return stripe.PaymentIntent.create(
            amount=amount,
            currency=settings.STRIPE_CURRENCY,
        )

    def render_checkout_page(request, order_form):
        if not stripe_public_key:
            messages.warning(
                request, 'Missing public key. Please set it in your environment.'  # noqa
                )
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': payment_intent.client_secret,
        }
        return render(request, 'checkout/checkout.html', context)

    current_basket = basket_contents(request)
    total = current_basket['grand_total']
    stripe_total = round(total * 100)

    payment_intent = create_payment_intent(stripe_total)
    print(payment_intent)

    basket = get_basket(request)
    if not basket:
        show_empty_basket_message(request)
        return redirect(reverse('products'))

    order_form = OrderForm()
    return render_checkout_page(request, order_form)
