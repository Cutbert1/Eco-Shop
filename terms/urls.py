from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_terms, name='view_terms'),
]
