from django.urls import path

from .views import homePage, Items, CartView, orders_view, order_view

urlpatterns = [
    path('', homePage, name='homePage'),
    path('shop', Items, name='items'),
    path('cart', CartView, name='cart'),
    path('orders', orders_view, name='orders'),
    path('orders/<int:pk>', order_view, name='order')
]