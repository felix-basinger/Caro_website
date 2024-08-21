from django.contrib import admin
from .models import Product, ProductImage, Tag
from modeltranslation.admin import TranslationAdmin

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 6  # Количество пустых форм для добавления новых изображений


class ProductAdmin(TranslationAdmin):
    list_display = ('name', 'price', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('tags',)
    inlines = [ProductImageInline]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
