from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_basket, name='view_basket'),
    path(
        'add/<item_id>/', views.add_item_to_basket, name='add_item_to_basket'
        ),
    path(
        'update/<item_id>/', views.update_basket_quantity, name='update_basket_quantity'  # noqa
        ),
    path(
        'remove/<item_id>/', views.remove_from_basket, name='remove_from_basket'  # noqa
        ),
]
