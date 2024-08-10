from django.urls import path, include
from .views import index, product_list, add_to_cart, view_cart, remove_from_cart, checkout, order_detail

urlpatterns = [
    path('', index, name='index'),
    path('products/', product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),  # Убедитесь, что этот маршрут соответствует функции
    path('password_reset/', include('django.contrib.auth.urls')),
]
