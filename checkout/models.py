import uuid
from django.db import models

from django.db.models import Sum
from django.conf import settings
from django.core.validators import MinValueValidator
from django_countries.fields import CountryField

from products.models import Product

# Create your models here.


class Order(models.Model):
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    customer_name = models.CharField(max_length=255)
    email = models.EmailField(blank=False, null=False)
    address = models.CharField(max_length=255, blank=False, null=False)
    phone_number = models.CharField(max_length=24, null=False, blank=False)
    city = models.CharField(max_length=100, null=False, blank=False)
    county = models.CharField(max_length=100, null=True, blank=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    zipcode = models.CharField(max_length=20, blank=True, null=True)
    country = CountryField(
        blank_label='Country *', blank=False, null=False
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivery_cost = models.DecimalField(
        max_digits=6, decimal_places=2, null=False, default=0
        )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
        )
    grand_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
        )
    existing_basket = models.TextField(null=False, blank=False, default='')
    stripe_payment_intent_id = models.CharField(
        max_length=255, null=False, default=''
        )

    def _generate_order_number(self):
        return uuid.uuid4().hex.upper()

    def update_total(self):
        self.order_total = self.calculate_order_total()
        self.delivery_cost = self.calculate_delivery_cost()
        self.grand_total = self.order_total + self.delivery_cost
        self.save()

    def calculate_order_total(self):
        return self.lineitems.aggregate(Sum('lineitem_total'))['lineitem_total__sum'] or 0  # noqa

    def calculate_delivery_cost(self):
        if self.order_total < settings.FREE_DELIVERY_THRESHOLD:
            return self.order_total * settings.STANDARD_DELIVERY_PERCENTAGE / 100  # noqa
        return 0

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_number

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderLineItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='lineitems'
        )
    product = models.ForeignKey(
        Product, null=False, blank=False, on_delete=models.CASCADE
        )
    quantity = models.PositiveIntegerField(
        null=False, blank=False, default=1, validators=[MinValueValidator(1)],
    )
    lineitem_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
    )

    def save(self, *args, **kwargs):
        self.lineitem_total = self.calculate_lineitem_total()
        super().save(*args, **kwargs)
        self.update_order_total()

    def calculate_lineitem_total(self):
        return self.product.price * self.quantity

    def update_order_total(self):
        self.order.update_total()

    def __str__(self):
        return f'SKU {self.product.sku} on order {self.order.order_number}'

    class Meta:
        verbose_name = 'Order Line Item'
        verbose_name_plural = 'Order Line Items'
