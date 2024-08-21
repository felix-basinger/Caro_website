from django import forms
from .models import CartItem


class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.HiddenInput(),
            'quantity': forms.HiddenInput(),
        }

