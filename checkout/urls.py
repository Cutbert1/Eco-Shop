from django.urls import path
from . import views
from .webhooks import stripe_webhook

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_complete/<order_number>', views.checkout_complete, name='checkout_complete'),  # noqa
    path('wh/', stripe_webhook, name='stripe_webhook'),
]
