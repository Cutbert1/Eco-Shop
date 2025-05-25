from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderLineItem
from products.models import Product
from profiles.models import AccountProfile

import stripe  # noqa
import json
import time


class WebhookHandler:
    """
    Handles Stripe webhooks and processes various event types.
    """

    MAX_ATTEMPTS = 5
    SLEEP_DURATION = 1

    def __init__(self, request):
        """
        Initialize the WebhookHandler with the incoming request.
        """
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order,
             'contact_email': settings.DEFAULT_FROM_EMAIL,
             'order_total': order.order_total,
             'delivery_cost': order.delivery_cost
             })

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic, unknown, or unexpected webhook event.
        """
        return self._create_response(event)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook event from Stripe.
        """
        try:
            payment_intent = event.data.object
            save_info = self._get_save_info(payment_intent)
            stripe_charge = self._retrieve_stripe_charge(
                payment_intent.latest_charge
            )

            basket = self._get_basket(payment_intent)

            order_data = self._extract_order_data(
                payment_intent, stripe_charge
                )

            order = self._get_order(order_data)

            if order:
                return self._handle_existing_order(event, order)
            else:
                order = self._create_order(order_data, basket)
                if not order:
                    return self._create_error_response(
                        event, "Failed to create order."
                    )
                self._create_order_line_items(order, basket)

                self._update_profile(payment_intent, save_info, order_data)

                return self._create_response(event)
        except Exception as e:
            return self._create_error_response(
                event, f"Error processing payment_intent.succeeded: {str(e)}"
            )

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook event from Stripe.
        """
        return self._create_response(event)

    def _get_save_info(self, payment_intent):
        """
        Safely get the save_info value from payment_intent metadata.
        """
        try:
            return payment_intent.metadata.save_info
        except AttributeError:
            return False

    def _get_basket(self, payment_intent):
        """
        Safely get the basket value from payment_intent metadata.
        """
        try:
            return payment_intent.metadata.basket
        except AttributeError:
            return ""

    def _extract_order_data(self, payment_intent, charge):
        """
        Extract order data from the payment intent and charge.
        """
        billing_details = charge.billing_details
        shipping = payment_intent.shipping

        grand_total = round(charge.amount / 100, 2)
        temp_order = Order(order_total=grand_total)
        delivery_cost = temp_order.calculate_delivery_cost()
        order_total = grand_total - delivery_cost

        return {
            'customer_name': billing_details.name,
            'email': billing_details.email,
            'phone_number': billing_details.phone,
            'address': json.dumps(self._sanitize_address(shipping.address)),
            'city': shipping.address.city,
            'county': shipping.address.state,
            'postcode': shipping.address.postal_code,
            'country': shipping.address.country,
            'grand_total': grand_total,
            'delivery_cost': delivery_cost,
            'order_total': order_total,
            'basket': self._get_basket(payment_intent),
            'stripe_payment_intent_id': payment_intent.id,
        }

    def _sanitize_address(self, address):
        """
        Sanitize address fields by replacing empty strings with None.
        """
        return {
            field: (value if value else None) for field, value in address.items()  # noqa
        }

    def _retrieve_stripe_charge(self, charge_id):
        """
        Retrieve the Stripe charge object.
        """
        return stripe.Charge.retrieve(charge_id)

    def _get_order(self, order_data):
        """
        Attempt to get the order object, trying 5 times.
        """
        for attempt in range(self.MAX_ATTEMPTS):
            try:
                return Order.objects.get(
                    customer_name__iexact=order_data['customer_name'],
                    email__iexact=order_data['email'],
                    phone_number__iexact=order_data['phone_number'],
                    address__iexact=order_data['address'],
                    city__iexact=order_data['city'],
                    county__iexact=order_data['county'],
                    postcode__iexact=order_data['postcode'],
                    country__iexact=order_data['country'],
                    grand_total=order_data['grand_total'],
                    existing_basket=order_data['basket'],
                    stripe_payment_intent_id=order_data[
                        'stripe_payment_intent_id'
                    ],
                )
            except Order.DoesNotExist:
                time.sleep(self.SLEEP_DURATION)
        return None

    def _handle_existing_order(self, event, order):
        """
        Handle the case where the order already exists.
        """
        try:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: order already in database',  # noqa
                status=200
            )
        except Exception as e:
            return self._create_error_response(
                event, f"Error sending confirmation email: {str(e)}"
            )

    def _create_order(self, order_data, basket,):
        """
        Create a new order in the database.
        """
        order = Order.objects.create(
            customer_name=order_data['customer_name'],
            # account_profile=['profile'],
            email=order_data['email'],
            phone_number=order_data['phone_number'],
            address=order_data['address'],
            city=order_data['city'],
            county=order_data['county'],
            postcode=order_data['postcode'],
            country=order_data['country'],
            grand_total=order_data['grand_total'],
            existing_basket=basket,
            stripe_payment_intent_id=order_data['stripe_payment_intent_id'],
            delivery_cost=order_data.get('delivery_cost', 0),
            order_total=order_data.get(
                'order_total', order_data['grand_total']
                )
        )
        try:
            self._send_confirmation_email(order)
        except Exception as e:
            print(f"Error sending confirmation email: {str(e)}")
        return order

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

    def _update_profile(self, payment_intent, save_info, order_data):
        """
        Update profile information if save_info was checked.
        """
        profile = None
        username = self._get_username(payment_intent)
        if username != 'AnonymousUser':
            try:
                profile = AccountProfile.objects.get(user__username=username)
                if save_info:
                    profile.primary_phone_number = order_data['phone_number']
                    profile.primary_country = order_data['country']
                    profile.primary_postcode = order_data['postcode']
                    profile.primary_city = order_data['city']
                    profile.primary_address = order_data['address']
                    profile.primary_county = order_data['county']
                    profile.save()
            except AccountProfile.DoesNotExist:
                pass

    def _get_username(self, payment_intent):
        """
        Safely get the username from payment_intent metadata.
        """
        try:
            return payment_intent.metadata.username
        except AttributeError:
            return 'AnonymousUser'
