from django.db import models

# Create your models here.


class Category(models.Model):
    """
    Includes a required internal name and an user-friendly
    display name. Categories ordered alphabetically by name.
    """
    name = models.CharField(max_length=200)
    friendly_name = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name or self.name


class Product(models.Model):
    """
    Each product belongs to an optional category, has a unique name and SKU,
    a detailed description, price, optional rating, timestamps for creation
    and updates, and product image.

    Products are ordered by creation date, newest first.
    """
    category = models.ForeignKey(
        "Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=200, unique=True)
    sku = models.CharField(max_length=200, unique=True, null=True, blank=True)
    description = models.TextField(verbose_name="Product Description")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    product_image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['-created_on']

    def __str__(self):
        return self.name
