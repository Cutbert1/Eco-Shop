from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_order_total_on_save(sender, instance, created, **kwargs):
    """
    Update the total of the order when a line item is created or updated.
    """
    _update_order_total(instance)


@receiver(post_delete, sender=OrderLineItem)
def update_order_total_on_delete(sender, instance, **kwargs):
    """
    Update the total of the order when a line item is deleted.
    """
    _update_order_total(instance)


def _update_order_total(line_item):
    line_item.order.update_total()
