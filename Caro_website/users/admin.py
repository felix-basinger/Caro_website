from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'paypal_order_id', 'status', 'total_amount', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('user__username', 'paypal_order_id', 'shipping_name')
    ordering = ['-created_at']
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('user', 'paypal_order_id', 'status', 'total_amount')
        }),
        ('Shipping Information', {
            'fields': ('shipping_name', 'shipping_address', 'shipping_city', 'shipping_state', 'shipping_zip_code',
                       'shipping_country')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
        }),
    )


admin.site.register(Order, OrderAdmin)


class CustomUserAdmin(UserAdmin):
    # Поля, которые будут отображаться в списке пользователей
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    # Поля, по которым можно фильтровать пользователей
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    # Поля, которые можно редактировать в форме изменения пользователя
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Поля, которые отображаются при создании пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    # По каким полям будет осуществляться поиск
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)


# Регистрируем модель пользователя с кастомным отображением в админке
admin.site.register(CustomUser, CustomUserAdmin)