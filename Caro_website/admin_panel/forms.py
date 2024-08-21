from django import forms
from shop.models import Product, Tag, ProductImage


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'price', 'tags']


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
