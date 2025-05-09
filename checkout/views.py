from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages

from products.models import Product
from .forms import OrderForm, Order
from basket.contexts import basket_contents
from .models import OrderLineItem

import stripe

# Create your views here.


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    def handle_post_request(request):
        basket = request.session.get('basket', {})
        order_form = OrderForm(get_form_data(request))

        if order_form.is_valid():
            order = order_form.save(commit=False)

            # Set up Stripe payment intent
            stripe.api_key = stripe_secret_key
            total = calculate_total(basket)
            stripe_total = round(total * 100)

            try:
                payment_intent = stripe.PaymentIntent.create(
                    amount=stripe_total,
                    currency=settings.STRIPE_CURRENCY,
                )
                order.stripe_pid = payment_intent.id
                order.save()
            except stripe.error.StripeError as e:
                messages.error(
                    request, f"An error occurred while processing your payment: {str(e)}"  # noqa
                    )
                order.delete()
                return redirect(reverse('view_basket'))

            if not process_order_line_items(basket, order):
                return redirect(reverse('view_basket'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse(
                'checkout_complete', args=[order.order_number]
            ))

        messages.error(
            request, 'Form error. Please recheck your details.'
            )
        return redirect(reverse('view_basket'))

    def get_form_data(request):
        return {
            'customer_name': request.POST['customer_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'address': request.POST['address'],
            'city': request.POST['city'],
            'county': request.POST['county'],
            'postcode': request.POST['postcode'],
            'zipcode': request.POST['zipcode'],
            'country': request.POST['country'],
        }

    def process_order_line_items(basket, order):
        try:
            for item_id, item_data in basket.items():
                product = Product.objects.get(id=item_id)
                OrderLineItem.objects.create(
                    order=order, product=product, quantity=item_data
                )
        except Product.DoesNotExist:
            messages.error(
                request, "One of the products in your basket wasn't found in our database. Please call us for assistance!"  # noqa
            )
            order.delete()
            return False
        return True

    def calculate_total(basket):
        total = sum(
            item_data * Product.objects.get(id=item_id).price for item_id, item_data in basket.items()  # noqa
            )
        return total

    def handle_get_request(request):
        basket = request.session.get('basket', {})
        if not basket:
            messages.error(request, "Your basket is currently empty")
            return redirect(reverse('products'))

        current_basket = basket_contents(request)
        total = current_basket['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=stripe_total, currency=settings.STRIPE_CURRENCY
            )
        except stripe.error.StripeError as e:
            messages.error(
                request, f"An error occurred while processing your payment: {str(e)}"  # noqa
            )
            return redirect(reverse('view_basket'))

        order_form = OrderForm()
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

    if request.method == 'POST':
        return handle_post_request(request)

    return handle_get_request(request)


def checkout_complete(request, order_number):
    """
    Handle successful checkouts and render the success page.

    Args:
        request: The HTTP request object.
        order_number: The unique identifier for the order.
    """
    save_info = request.session.get('save_info')  # noqa
    order = get_object_or_404(Order, order_number=order_number)

    messages.success(request, (
        f'Order completed! Your order number is {order_number}. '
        f'Confirmation email has beeen sent to {order.email}.'
    ))

    request.session.pop('basket', None)

    return render(request, 'checkout/checkout_complete.html', {'order': order})
