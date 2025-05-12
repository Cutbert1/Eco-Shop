from django.http import HttpResponse
from .models import Order, OrderLineItem
from products.models import Product

import stripe
import json
import time


class WebhookHandler:
    """
    Handles Stripe webhooks and processes various event types.
    """

    MAX_ATTEMPTS = 4
    SLEEP_DURATION = 1

    def __init__(self, request):
        """
        Initialize the WebhookHandler with the incoming request.
        """
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic, unknown, or unexpected webhook event.
        """
        return self._create_response(event)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook event from Stripe.
        """
        payment_intent = event.data.object
        order_data = self._extract_order_data(payment_intent)
        stripe_charge = self._retrieve_stripe_charge(  # noqa
            payment_intent.latest_charge
            )

        if self._order_exists(order_data):
            return self._handle_existing_order(event)

        order = self._create_order(order_data, payment_intent.metadata.basket)
        if not order:
            return self._create_error_response(
                event, "Failed to create order."
                )

        self._create_order_line_items(order, order_data.basket)
        return self._create_response(event)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook event from Stripe.
        """
        return self._create_response(event)

    def _extract_order_data(self, payment_intent):
        """
        Extract order data from the payment intent.
        """
        billing_details = payment_intent.latest_charge.billing_details
        return {
            'customer_name': billing_details.name,
            'email': billing_details.email,
            'phone_number': billing_details.phone,
            'address': self._sanitize_address(payment_intent.shipping.address),
            'city': payment_intent.shipping.city,
            'county': payment_intent.shipping.county,
            'postcode': payment_intent.shipping.postal_code,
            'zipcode': payment_intent.shipping.zipcode,
            'country': payment_intent.shipping.country,
            'grand_total': round(payment_intent.latest_charge.amount / 100, 2),
            'basket': payment_intent.metadata.basket,

        }

    def _sanitize_address(self, address):
        """
        Sanitize address fields by replacing empty strings with None.
        """
        return {
            field: (
                value if value else None
                ) for field, value in address.items()
            }

    def _retrieve_stripe_charge(self, charge_id):
        """
        Retrieve the Stripe charge object.
        """
        return stripe.Charge.retrieve(charge_id)

    def _order_exists(self, order_data):
        """
        Check if an order already exists in the database.
        """
        for attempt in range(self.MAX_ATTEMPTS):
            try:
                Order.objects.get(
                    customer_name__iexact=order_data['name'],
                    email__iexact=order_data['email'],
                    phone_number__iexact=order_data['phone'],
                    address__iexact=order_data['address'],
                    city__iexact=order_data['city'],
                    county__iexact=order_data['county'],
                    postcode__iexact=order_data['postcode'],
                    zipcode__iexact=order_data['zipcode'],
                    country__iexact=order_data['country'],
                    grand_total=order_data['grand_total'],
                    existing_basket=order_data['existing_basket'],
                    stripe_payment_intent_id=order_data['stripe_payment_intent_id'],  # noqa
                )
                return True
            except Order.DoesNotExist:
                time.sleep(self.SLEEP_DURATION)
        return False

    def _handle_existing_order(self, event):
        """
        Handle the case where the order already exists.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: order already in database',  # noqa
            status=200
        )

    def _create_order(self, order_data, basket):
        """
        Create a new order in the database.
        """
        try:
            order = Order.objects.create(
                customer_name=order_data['name'],
                email=order_data['email'],
                phone_number=order_data['phone'],
                address=order_data['address'],
                city=order_data['city'],
                county=order_data['county'],
                postcode=order_data['postcode'],
                zipcode=order_data['zipcode'],
                country=order_data['country'],
                grand_total=order_data['grand_total'],
            )
            return order
        except Exception as e:  # noqa
            return None

    def _create_order_line_items(self, order, basket):
        """
        Create order line items based on the basket data.
        """
        for item_id, item_data in json.loads(basket).items():
            product = Product.objects.get(id=item_id)
            if isinstance(item_data, int):
                OrderLineItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item_data,
                )

    def _create_error_response(self, event, error_message):
        """
        Create an error response for the webhook event.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | ERROR: {error_message}',  # noqa
            status=500
        )

    def _create_response(self, event):
        """
        Create an HTTP response for the given events.
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
