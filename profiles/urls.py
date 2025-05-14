from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path(
        'order_record/<order_number>', views.order_record, name='order_record'
        ),
]
