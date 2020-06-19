from django.urls import path 
from . import views 

urlpatterns = [
    path('courses/', views.AddToCart.as_view(), name='add_to_cart'),
]