from django.db import models

from django.conf import settings
from django.db import models
from shop.models import Product


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Cart {self.id} for {self.user}'

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.quantity} of {self.product.name}'

    def get_total_price(self):
        if self.product.discount and self.product.discount.is_active:
            return self.quantity * self.product.discounted_price
        return self.quantity * self.product.price
