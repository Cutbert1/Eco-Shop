from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import WebhookHandler  # noqa

import stripe


@require_POST
@csrf_exempt
def stripe_webhook(request):
    """Handle incoming webhooks from Stripe."""
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    event = verify_webhook_signature(payload, sig_header)
    if event is None:
        return HttpResponse(status=400)

    handler = WebhookHandler(request)

    event_map = {
        'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
        'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,  # noqa
    }

    event_type = event['type']

    event_handler = event_map.get(event_type, handler.handle_event)

    response = event_handler(event)
    return response


def verify_webhook_signature(payload, sig_header):
    """Verify the webhook signature and return the event if valid."""
    try:
        return stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        # Log the error for debugging purposes (optional)
        print(f"Webhook verification failed: {str(e)}")
        return HttpResponse(status=400)
    except Exception as e:
        # Handle unexpected errors
        print(f"An unexpected error occurred: {str(e)}")
        return HttpResponse(content=e, status=400)
