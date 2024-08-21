from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('about/', views.about, name='about'),
    path('new_index/', views.new_index, name='new_index'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('furniture/', views.furniture, name='furniture'),
    path('watch/', views.watch, name='watch'),
    path('fabrics/', views.fabrics, name='fabrics'),
    path('realty/', views.realty, name='realty'),
    path('add_to_favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<int:product_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('search/', views.search, name='search'),
    path('tag/<str:tag_name>/', views.product_by_tag, name='product_by_tag'),
    path('get-favorites-status/', views.get_favorites_status, name='get_favorites_status'),
    path('toggle-cart-item/<int:product_id>/', views.toggle_cart_item, name='toggle_cart_item'),
    path('get-cart-status/', views.get_cart_status, name='get_cart_status'),
]
