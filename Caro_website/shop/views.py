from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django_user_agents.utils import get_user_agent
from .models import Product, Favorite, Tag
from cart.models import Cart, CartItem


def new_index(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'shop/mobile/new_index.html'
    elif user_agent.is_tablet:
        template = 'shop/tablet/new_index.html'
    else:
        template = 'shop/new_index.html'
    return render(request, template)


def about(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'shop/mobile/about.html'
    elif user_agent.is_tablet:
        template = 'shop/tablet/about.html'
    else:
        template = 'shop/about.html'
    return render(request, template)


def product_list(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'shop/mobile/index.html'
    elif user_agent.is_tablet:
        template = 'shop/tablet/index.html'
    else:
        template = 'shop/index.html'

    products = Product.objects.all().order_by('-created_at')

    favorite_product_ids = []
    if request.user.is_authenticated:
        favorite_product_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        session_key = request.session.session_key
        if session_key:
            favorite_product_ids = Favorite.objects.filter(session_key=session_key).values_list('product_id', flat=True)

    return render(request, template, {
        'products': products,
        'favorite_product_ids': list(favorite_product_ids),
    })


def product_by_tag(request, tag_name):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'shop/mobile/product_by_tag.html'
    elif user_agent.is_tablet:
        template = 'shop/tablet/product_by_tag.html'
    else:
        template = 'shop/product_by_tag.html'

    tag = Tag.objects.filter(name=tag_name).first()
    products = []
    if tag:
        products = tag.products.all().order_by('-created_at')
    return render(request, template, {'products': products, 'tag': tag})


def product_detail(request, pk):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'shop/mobile/product_detail.html'
    elif user_agent.is_tablet:
        template = 'shop/tablet/product_detail.html'
    else:
        template = 'shop/product_detail.html'

    product = get_object_or_404(Product, pk=pk)
    return render(request, template, {'product': product})


def furniture(request):
    # Логика для раздела Furniture
    return render(request, 'furniture.html')


def watch(request):
    # Логика для раздела Watch
    return render(request, 'watch.html')


def fabrics(request):
    # Логика для раздела Fabrics
    return render(request, 'fabrics.html')


def realty(request):
    # Логика для раздела Realty
    return render(request, 'realty.html')


@require_POST
def add_to_favorites(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    if request.user.is_authenticated:
        favorite = Favorite.objects.filter(user=request.user, product=product)
    else:
        favorite = Favorite.objects.filter(session_key=session_key, product=product)

    if favorite.exists():
        favorite.delete()
        action = 'removed'
    else:
        if request.user.is_authenticated:
            Favorite.objects.create(user=request.user, product=product)
        else:
            Favorite.objects.create(session_key=session_key, product=product)
        action = 'added'

    # Добавьте это для отладки
    print(f'Action: {action}, Product ID: {product_id}, Session Key: {session_key}, User: {request.user}')

    return JsonResponse({'status': action, 'product_id': product_id})


def remove_from_favorites(request, product_id):
    session_key = request.session.session_key
    if request.user.is_authenticated:
        favorite = Favorite.objects.filter(user=request.user, product_id=product_id)
    else:
        favorite = Favorite.objects.filter(session_key=session_key, product_id=product_id)

    favorite.delete()

    return JsonResponse({'status': 'ok', 'product_id': product_id})


def favorites_list(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'shop/mobile/favorites_list.html'
    elif user_agent.is_tablet:
        template = 'shop/tablet/favorites_list.html'
    else:
        template = 'shop/favorites_list.html'

    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        favorites = Favorite.objects.filter(session_key=session_key)

    products = [favorite.product for favorite in favorites]
    favorite_product_ids = [favorite.product.id for favorite in favorites]

    return render(request, template, {
        'products': products,
        'favorite_product_ids': favorite_product_ids,
    })


def search(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'shop/mobile/search_results.html'
    elif user_agent.is_tablet:
        template = 'shop/tablet/search_results.html'
    else:
        template = 'shop/search_results.html'

    query = request.GET.get('q')
    results = []
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(tags__name__icontains=query)
        ).distinct().order_by('-created_at')
    return render(request, template, {'results': results, 'query': query})


@login_required
def get_favorites_status(request):
    product_ids = request.GET.getlist('product_ids[]')
    favorites = Favorite.objects.filter(user=request.user, product_id__in=product_ids)
    favorite_product_ids = favorites.values_list('product_id', flat=True)
    return JsonResponse({'favorites': list(favorite_product_ids)})


@login_required
def toggle_cart_item(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item = CartItem.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.delete()
        status = 'removed'
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        status = 'added'

    return JsonResponse({
        'status': status,
        'quantity': cart.get_total_quantity(),
    })


@login_required
def get_cart_status(request):
    cart = Cart.objects.filter(user=request.user).first()
    if not cart:
        return JsonResponse({'cart_items': []})

    cart_items = cart.items.values_list('product_id', flat=True)
    return JsonResponse({'cart_items': list(cart_items)})
