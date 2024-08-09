from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem


def index(request):
    # Отображение продуктов на главной странице с пагинацией
    product_list = Product.objects.all().order_by('id')
    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/index.html', {'page_obj': page_obj})


@login_required
def product_list(request):
    # Отображение списка продуктов с пагинацией
    product_list = Product.objects.all().order_by('id')
    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/product_list.html', {'page_obj': page_obj})


@login_required
def add_to_cart(request, product_id):
    # Добавление товара в корзину
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    # Если товар уже в корзине, увеличиваем количество
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    # Обновление итоговой суммы корзины
    cart.update_total_price()
    return redirect('index')


@login_required
def view_cart(request):
    # Просмотр корзины
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': cart.total_price})


@login_required
def remove_from_cart(request, cart_item_id):
    # Удаление товара из корзины или уменьшение количества
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    # Обновление итоговой суммы корзины
    cart_item.cart.update_total_price()
    return redirect('view_cart')

@login_required
def checkout(request):
    # Получение корзины текущего пользователя
    cart = get_object_or_404(Cart, user=request.user)

    if request.method == 'POST':
        # Логика для оформления заказа
        order = Order.objects.create(user=request.user, status='pending')
        for item in cart.items.all():
            order.products.add(item.product)
        cart.items.all().delete()  # Очистка корзины
        cart.update_total_price()
        return redirect('order_detail', id=order.id)

    return render(request, 'shop/checkout.html', {'cart': cart})