from django.http import HttpResponse


class WebhookHandler:
    """
    Handles Stripe webhooks and processes various event types.
    """

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
        return self._create_response(event)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook event from Stripe.
        """
        return self._create_response(event)

    def _create_response(self, event):
        """
        Create an HTTP response for the given events
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200
        )
