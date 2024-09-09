from django.conf import settings
from django.db import models
from django.utils import timezone


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=0)  # Процент скидки
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    active = models.BooleanField(default=True)
    added_to_sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.discount_percent}%)"

    @property
    def is_active(self):
        now = timezone.now()
        return self.active and self.start_date <= now <= self.end_date


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', default='images/noimage_detail.png')
    tags = models.ManyToManyField(Tag, related_name='products')
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def discounted_price(self):
        if self.discount and self.discount.is_active:
            return self.price * (1 - self.discount.discount_percent / 100)
        return self.price


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return f"Image for {self.product.name}"


class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)  # Добавляем поле для времени добавления

    class Meta:
        unique_together = ('user', 'session_key', 'product')
        ordering = ['-added_at']

    def __str__(self):
        return f"{self.user or self.session_key} - {self.product.name}"
