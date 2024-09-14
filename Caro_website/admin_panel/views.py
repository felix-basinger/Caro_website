from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from shop.models import Product, Tag, ProductImage
from .forms import ProductForm, TagForm, ProductImageForm, DiscountForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django_user_agents.utils import get_user_agent

from shop.models import Discount


def admin_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func


@admin_required
def admin_dashboard(request):
    user_agent = get_user_agent(request)

    if user_agent.is_mobile:
        template = 'admin_panel/admin_dashboard_mobile.html'
    else:
        template = 'admin_panel/admin_dashboard.html'

    products = Product.objects.all().order_by('-created_at')
    tags = Tag.objects.all()
    discounts = Discount.objects.all()
    return render(request, template, {'products': products, 'tags': tags, 'discounts': discounts})


@admin_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.images.exists():
        images = [{'id': image.id, 'url': image.image.url} for image in product.images.all()]
    else:
        images = [{'id': None, 'url': product.image.url}]
    product_data = {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity': product.quantity,
        'tags': [{'id': tag.id, 'name': tag.name} for tag in product.tags.all()],
        'images': [{'id': image.id, 'url': image.image.url} for image in product.images.all()]
    }
    return JsonResponse(product_data)


@admin_required
@require_POST
def product_create(request):
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
        product = form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@admin_required
@require_POST
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@admin_required
@require_POST
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return JsonResponse({'success': True})


@admin_required
def product_images(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            product_image = form.save(commit=False)
            product_image.product = product
            product_image.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        product_data = {
            'id': product.id,
            'name': product.name,
            'images': [{'id': image.id, 'url': image.image.url} for image in product.images.all()]
        }
        return JsonResponse(product_data)


@admin_required
@require_POST
def image_delete(request, pk):
    image = get_object_or_404(ProductImage, pk=pk)
    image.delete()
    return JsonResponse({'success': True})


@admin_required
def tag_detail(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    return JsonResponse({'id': tag.id, 'name': tag.name})


@admin_required
@require_POST
def tag_create(request):
    form = TagForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@admin_required
@require_POST
def tag_edit(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    form = TagForm(request.POST, instance=tag)
    if form.is_valid():
        form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@admin_required
@require_POST
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    tag.delete()
    return JsonResponse({'success': True})


@admin_required
def discount_list(request):
    discounts = Discount.objects.all()
    return render(request, 'admin_panel/discount_list.html', {'discounts': discounts})


@admin_required
def discount_detail(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    data = {
        'id': discount.id,
        'name': discount.name,
        'discount_percent': discount.discount_percent,
        'start_date': discount.start_date.strftime('%Y-%m-%dT%H:%M'),
        'end_date': discount.end_date.strftime('%Y-%m-%dT%H:%M'),
    }
    return JsonResponse(data)


@admin_required
@require_POST
def discount_create(request):
    form = DiscountForm(request.POST)
    if form.is_valid():
        discount = form.save(commit=False)
        print(f"Start Date: {discount.start_date}, End Date: {discount.end_date}")
        print(f"Is Active (before save): {discount.is_active}")
        discount.save()
        print(f"Is Active (after save): {discount.is_active}")
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@admin_required
@require_POST
def discount_edit(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    form = DiscountForm(request.POST, instance=discount)
    if form.is_valid():
        discount = form.save(commit=False)
        print(f"Start Date: {discount.start_date}, End Date: {discount.end_date}")
        print(f"Is Active (before save): {discount.is_active}")
        discount.save()
        print(f"Is Active (after save): {discount.is_active}")
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@admin_required
def discount_delete(request, pk):
    discount = get_object_or_404(Discount, pk=pk)
    discount.delete()
    return JsonResponse({'success': True})
