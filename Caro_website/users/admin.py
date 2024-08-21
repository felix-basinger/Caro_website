from django.contrib import admin

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
