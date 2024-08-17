from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    index,
    product_list,
    add_to_cart,
    view_cart,
    remove_from_cart,
    checkout,
    order_preview,
    confirm_order,
    order_detail,
    confirm_logout,
    product_detail,
    add_review,
    orders_report
)

urlpatterns = [
    path('', index, name='index'),
    path('products/', product_list, name='product_list'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('remove_from_cart/<int:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('checkout/', checkout, name='checkout'),
    path('order/preview/<int:order_id>/', order_preview, name='order_preview'),
    path('order/confirm/<int:order_id>/', confirm_order, name='confirm_order'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('accounts/logout/', LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('accounts/logout/confirm/', LogoutView.as_view(template_name='account/confirm_logout.html'), name='logout_confirmed'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    path('product/<int:product_id>/add_review/', add_review, name='add_review'),
    path('orders_report/', orders_report, name='orders_report'),
]

