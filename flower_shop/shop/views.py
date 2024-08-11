from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Category, Order, OrderItem  # Импортируйте OrderItem
from .forms import ProductFilterForm

def index(request):
    # Отображение продуктов на главной странице с пагинацией
    product_list = Product.objects.all().order_by('id')
    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/index.html', {'page_obj': page_obj})

def product_list(request):
    product_list = Product.objects.all().order_by('id')
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data['category']:
            product_list = product_list.filter(category=form.cleaned_data['category'])
        if form.cleaned_data['min_price']:
            product_list = product_list.filter(price__gte=form.cleaned_data['min_price'])
        if form.cleaned_data['max_price']:
            product_list = product_list.filter(price__lte=form.cleaned_data['max_price'])
        if form.cleaned_data['search_query']:
            product_list = product_list.filter(name__icontains=form.cleaned_data['search_query'])

    # Отладочная информация
    print("Форма:", form)
    print("Данные формы:", form.cleaned_data)
    print("Количество товаров:", product_list.count())

    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/product_list.html', {'page_obj': page_obj, 'form': form})

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
    # Если корзина не существует, она будет создана
    cart, created = Cart.objects.get_or_create(user=request.user)
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
    cart = get_object_or_404(Cart, user=request.user)

    if request.method == 'POST':
        # Создание нового заказа
        order = Order.objects.create(user=request.user, status='pending')

        # Добавление товаров из корзины в заказ
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

        # Очистка корзины
        cart.items.all().delete()

        # Обновление итоговой суммы заказа
        order.update_total_price()

        return redirect('order_detail', order_id=order.id)

    return render(request, 'shop/checkout.html', {'cart': cart})

@login_required
def order_detail(request, order_id):
    # Получение заказа по идентификатору
    order = get_object_or_404(Order, id=order_id)

    # Отображение страницы с деталями заказа
    return render(request, 'shop/order_detail.html', {'order': order})
