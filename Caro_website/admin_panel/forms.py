from django import forms
from shop.models import Product, Tag, ProductImage

from shop.models import Discount


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'quantity', 'tags', 'discount']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
            'discount': forms.Select(),
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['name', 'discount_percent', 'start_date', 'end_date']
