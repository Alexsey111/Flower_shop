from django.contrib import admin
from .models import Product, Order, Review, Report, Cart, CartItem, Category, DeliveryMethod, PaymentMethod

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Category)

@admin.register(DeliveryMethod)
class DeliveryMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost')

@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'order', 'profit', 'expenses')

