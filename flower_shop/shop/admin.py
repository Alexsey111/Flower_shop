from django.contrib import admin
from .models import Product, Order, Review, Report, Cart, CartItem, Category

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Report)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)
