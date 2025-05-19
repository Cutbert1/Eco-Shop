from django.contrib import admin  # noqa
from django.urls import path
from . import views

urlpatterns = [
    path('', views.fetch_all_products, name='products'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path(
        'update/<int:product_id>/', views.update_product, name='update_product'
        ),
    path(
        'delete/<int:product_id>/', views.delete_product, name='delete_product'
        ),
]
