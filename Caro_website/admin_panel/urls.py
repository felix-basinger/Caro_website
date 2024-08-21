from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('products/<int:pk>/', views.product_detail, name='product_details'),
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('products/<int:pk>/images/', views.product_images, name='product_images'),
    path('images/<int:pk>/delete/', views.image_delete, name='image_delete'),
    path('tags/<int:pk>/', views.tag_detail, name='tag_detail'),
    path('tags/create/', views.tag_create, name='tag_create'),
    path('tags/<int:pk>/edit/', views.tag_edit, name='tag_edit'),
    path('tags/<int:pk>/delete/', views.tag_delete, name='tag_delete'),
]
