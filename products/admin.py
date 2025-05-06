from django.contrib import admin
from .models import Product, Category

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'name',
        'price',
        'sku',
        'rating',
        'created_on',
        'updated_on',
        'product_image',
    )
    ordering = ('-created_on',)

    list_filter = ('category', 'rating', 'created_on')
    search_fields = ('name', 'sku', 'category__name')


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'friendly_name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
