from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.order_create, name='order_create'),
]