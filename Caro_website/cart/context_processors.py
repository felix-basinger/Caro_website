from .models import Cart


def cart_total_quantity(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        total_quantity = cart.get_total_quantity()
    else:
        total_quantity = 0
    return {'cart_total_quantity': total_quantity}
