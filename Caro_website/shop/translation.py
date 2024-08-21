from modeltranslation.translator import register, TranslationOptions
from .models import Product, Tag


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description')
