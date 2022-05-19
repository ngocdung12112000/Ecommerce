from django.contrib import admin
from .models import Item, OrderItem, Order, Address

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'price', 'discount_price', 'description']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['street_address', 'apartment_address',
     'country', 'zip', 'default']

# Register your models here.
admin.site.register(Item,ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address, AddressAdmin)