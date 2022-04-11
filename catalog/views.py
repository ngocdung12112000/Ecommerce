from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order
from django.views.generic import ListView, DetailView, View
from django.contrib import messages
from django.utils import timezone

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
            return redirect('details', slug=slug)
        else:
            order.items.add(order_item)
            order.save()
            messages.success(request, f"{item} was added to your cart")
            return redirect('details', slug=slug)
    else:
        # ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered=False)  # ordered_date=ordered_date)
        order.items.add(order_item)
        order.save()
        messages.success(request, f"{item} was added to your cart")
        return redirect('details', slug=slug)

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
            return redirect('details', slug=slug)
        else:
            messages.info(request, f"{item} was not in your cart")
            return redirect('details', slug=slug)
    else:
        messages.info(request, "You don't have an active order")
        return redirect('details', slug=slug)