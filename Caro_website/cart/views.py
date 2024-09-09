from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Cart, CartItem
from shop.models import Product
from django_user_agents.utils import get_user_agent


@login_required
def cart_detail(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'cart/cart_detail_mobile.html'
    else:
        template = 'cart/cart_detail.html'

    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all().order_by('order')

    return render(request, template, {'cart': cart, 'items': items})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'quantity': cart.get_total_quantity()})
    return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart:cart_detail')


@login_required
def update_cart_item_quantity(request, item_id, action):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart = cart_item.cart

    if action == 'increase':
        cart_item.quantity += 1
        cart_item.save()
    elif action == 'decrease':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    cart_total_price = sum(item.get_total_price() for item in cart.items.all())

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'item_id': cart_item.id,
            'quantity': cart_item.quantity,
            'item_total_price': cart_item.get_total_price(),
            'cart_total_price': cart_total_price
        })

    return redirect('cart:cart_detail')


@login_required
def get_cart_status(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return JsonResponse({'cart_items': []})

    cart_items = cart.items.values_list('product_id', flat=True)
    return JsonResponse({'cart_items': list(cart_items)})


