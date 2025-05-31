from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_privacy, name='view_privacy'),
]
