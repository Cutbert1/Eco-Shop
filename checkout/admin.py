from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Displays order line items in a tabular format within the
    Order admin page. Makes the line item total read-only.
    """
    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    Provides:
    - Inline editing of related OrderLineItems.
    - Read-only fields for computed values and
      details of  values that connot be changed.
    - Custom layout for the edit form.
    - List display, ordering, filtering, and search capabilities.
    """
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number', 'created_at',
        'delivery_cost', 'order_total',
        'grand_total', 'existing_basket', 'stripe_payment_intent_id'
    )

    fields = (
        'customer_name', 'order_number', 'account_profile', 'created_at',
        'email', 'phone_number', 'address', 'city', 'postcode',
        'county', 'country', 'delivery_cost',
        'order_total', 'grand_total', 'existing_basket',
        'stripe_payment_intent_id'
    )

    list_display = (
        'customer_name', 'order_number', 'created_at',
        'delivery_cost', 'order_total', 'grand_total',
    )

    ordering = ('-created_at',)

    list_filter = ('created_at', 'order_number', 'customer_name')
    search_fields = ('order_number', 'customer_name', 'email')


admin.site.register(Order, OrderAdmin)
