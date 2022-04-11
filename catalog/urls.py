from django.urls import path
from .views import (HomeView,
    shop, 
    checkout, 
    contact, 
    ItemDetailView, 
    CartView,
    ShopView,
    cart, 
    add_to_cart,
    remove_from_cart,
    details
 )

urlpatterns = [
    path('shop/', ShopView.as_view(), name='shop'),
    path('checkout/', checkout, name='checkout'),
    path('contact/', contact, name='contact'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    # path('details/', details, name='details'),
    path('details/<slug>/', ItemDetailView.as_view(), name='details'),
    path('cart/', CartView.as_view(), name='cart'),
    # path('cart/', cart, name='cart'),
    path('', HomeView.as_view(), name='home'),
]