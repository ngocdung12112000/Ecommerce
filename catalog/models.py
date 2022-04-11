from email.mime import image
from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.

class Item(models.Model):
    title = models.CharField(max_length=150)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField(default='default.jpg',
                              upload_to='product_images')

    def __str__(self):
        return self.title

    def get_add_to_cart_url(self):
        return reverse('add_to_cart', kwargs={'slug': self.slug}) 

    def get_remove_from_cart_url(self):
        return reverse('remove_from_cart', kwargs={'slug': self.slug})  
    

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_item_price(self):
        real_price = self.item.price if self.item.discount_price == 0 else self.item.discount_price
        return real_price * self.quantity

class Order(models.Model):
    items = models.ManyToManyField(OrderItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
