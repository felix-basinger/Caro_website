from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, blank=False, null=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Измените related_name
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Измените related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    full_name = models.CharField(max_length=30, blank=True)
    shipping_last_name = models.CharField(max_length=30, blank=True)
    shipping_address = models.CharField(max_length=50, blank=True)
    billing_first_name = models.CharField(max_length=30, blank=True)
    billing_last_name = models.CharField(max_length=30, blank=True)
    billing_address = models.CharField(max_length=50, blank=True)
    payment = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    paypal_order_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Данные о доставке
    shipping_name = models.CharField(max_length=255)
    shipping_address = models.CharField(max_length=255)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_zip_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100)

    def __str__(self):
        return f"Order {self.id} by {self.user.username} - {self.status}"

    class Meta:
        ordering = ['-created_at']
