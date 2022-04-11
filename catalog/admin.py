from django.contrib import admin
from .models import Item, OrderItem, Order

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'price', 'discount_price', 'description']

# Register your models here.
admin.site.register(Item,ItemAdmin)
admin.site.register(OrderItem)
admin.site.register(Order)