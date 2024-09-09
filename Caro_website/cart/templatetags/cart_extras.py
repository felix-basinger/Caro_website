from django import template

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg


@register.simple_tag
def total_cart_price(cart):
    return sum(item.product.price * item.quantity for item in cart.items.all())


@register.filter
def get_cart_total_price(items):
    return sum(item.get_total_price() for item in items)
