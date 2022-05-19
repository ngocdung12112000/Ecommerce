from re import template
from django.urls import path
from django.contrib.auth import views
from .views import (HomeView,
    shop, 
    checkout, 
    contact, 
    signup,
    login_form,
    ItemDetailView, 
    CartView,
    ShopView,
    CheckoutView,
    cart, 
    add_to_cart,
    remove_from_cart,
    remove_single_from_cart,
    details
 )

urlpatterns = [
    path('shop/', ShopView.as_view(), name='shop'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('signup/', signup, name='signup'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('login/', views.LoginView.as_view(template_name='login.html'), name='login_form'),
    path('contact/', contact, name='contact'),
    path('add-to-cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('remove-single-from-cart/<slug>/', remove_single_from_cart, name='remove_single_from_cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    # path('details/', details, name='details'),
    path('details/<slug>/', ItemDetailView.as_view(), name='details'),
    path('cart/', CartView.as_view(), name='cart'),
    # path('cart/', cart, name='cart'),
    path('', HomeView.as_view(), name='home'),
]