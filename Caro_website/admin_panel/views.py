from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from shop.models import Product, Tag, ProductImage
from .forms import ProductForm, TagForm, ProductImageForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django_user_agents.utils import get_user_agent


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

    products = Product.objects.all()
    tags = Tag.objects.all()
    return render(request, template, {'products': products, 'tags': tags})


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
        'tags': [{'id': tag.id, 'name': tag.name} for tag in product.tags.all()],
        'images': [{'id': image.id, 'url': image.image.url} for image in product.images.all()]
    }
    return JsonResponse(product_data)


@admin_required
@require_POST
def product_create(request):
    form = ProductForm(request.POST, request.FILES)  # Передаем request.FILES для обработки изображений
    if form.is_valid():
        product = form.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'errors': form.errors}, status=400)


@admin_required
@require_POST
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    form = ProductForm(request.POST, request.FILES, instance=product)  # Также передаем request.FILES
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
