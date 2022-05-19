from cmath import log
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order, Address
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.utils import timezone
from .forms import AddressForm, SignUpForm
from django.contrib.auth import login
# Create your views here.


class HomeView(ListView):
    model = Item
    template_name = 'index.html'

class ShopView(ListView):
    model = Item
    template_name = 'shop.html'

class ItemDetailView(DetailView):
    model = Item
    template_name = 'detail.html'  

class CartView(View): #order_summary
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, 'cart.html', context)
            
        
# def home(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, 'index.html', context)

def shop(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'shop.html',context)

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()  
    return render(request, 'signup.html', {'form': form})

def login_form(request):
    return render(request, 'login.html')

class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, 'cart.html', context)
        except ObjectDoesNotExist:
            messages.success(self.request, "You dont have an active order")
            return redirect('home')

class CheckoutView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = AddressForm()
        context = {
            'form': form
        }
        return render(self.request, 'checkout.html', context)
    
    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        form = AddressForm(self.request.POST or None)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            apartment_address = form.cleaned_data.get('apartment_address')
            country = form.cleaned_data.get('country')
            zip = form.cleaned_data.get('zip')
            payment_option = form.cleaned_data.get('payment_option')
            address = Address(
                user=self.request.user,
                street_address=street_address,
                apartment_address=apartment_address,
                country=country,
                zip=zip,
                payment_option=payment_option
            )
            address.save()

            order.address = address
            order.save()
            return redirect('checkout')
        else:
            print('form is not valid')
            return redirect('checkout')
            # form.save()
            # return redirect('checkout')

def checkout(request):
    return render(request, 'checkout.html')

def contact(request):
    return render(request, 'contact.html')

def cart(request):
    return render(request, 'cart.html')

def details(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, 'detail.html',context) 

def cart(request):
    return render(request, 'cart.html') 


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.success(request, f"{item}'s quantity was updated")
            # return redirect('details', slug=slug)
            return redirect('cart')
        else:
            order.items.add(order_item)
            order.save()
            messages.success(request, f"{item} was added to your cart")
            # return redirect('details', slug=slug)
            return redirect('cart')
    else:
        # ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered=False)  # ordered_date=ordered_date)
        order.items.add(order_item)
        order.save()
        messages.success(request, f"{item} was added to your cart")
        # return redirect('details', slug=slug)
        return redirect('cart')

def remove_single_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:                
                order.items.remove(order_item)
                order.save()
            messages.success(request, f"{item} was removed from your cart")
            # return redirect('details', slug=slug)
            return redirect('cart')
        else:
            messages.info(request, f"{item} was not in your cart")
            # return redirect('details', slug=slug)
            return redirect('cart')
    else:
        messages.info(request, "You don't have an active order")
        # return redirect('details', slug=slug)
        return redirect('cart')        

def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False,
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order.items.remove(order_item)
            order.save()
            messages.success(request, f"{item} was removed from your cart")
            # return redirect('details', slug=slug)
            return redirect('cart')
        else:
            messages.info(request, f"{item} was not in your cart")
            # return redirect('details', slug=slug)
            return redirect('cart')
    else:
        messages.info(request, "You don't have an active order")
        # return redirect('details', slug=slug)
        return redirect('cart')