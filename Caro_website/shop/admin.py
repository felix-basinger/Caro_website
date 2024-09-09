from django.contrib import admin
from .models import Product, ProductImage, Tag, Discount
from modeltranslation.admin import TranslationAdmin


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 6  # Количество пустых форм для добавления новых изображений


class ProductAdmin(TranslationAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('tags',)
    inlines = [ProductImageInline]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'discount_percent', 'start_date', 'end_date', 'active', 'is_active')
    list_filter = ('active', 'start_date', 'end_date')
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
