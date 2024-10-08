from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Product, Cart, CartItem, Category, Order, OrderItem, DeliveryMethod, PaymentMethod, Report, Review
from .forms import ProductFilterForm, CheckoutForm, OrderPreviewForm, OrderForm, ConfirmLogoutForm, ReviewForm
from .utils import calculate_profit, calculate_expenses
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum, Avg
from django.contrib.auth import logout


def index(request):
    products = Product.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # Добавляем форму для отзывов
    form = ReviewForm()

    return render(request, 'shop/index.html', {
        'page_obj': page_obj,
        'form': form,
    })

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

    paginator = Paginator(product_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Отображаем форму для добавления отзыва
    review_form = ReviewForm()

    return render(request, 'shop/product_list.html', {
        'page_obj': page_obj,
        'form': form,
        'review_form': review_form,
    })

# def add_review(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if request.method == 'POST':
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.user = request.user
#             review.product = product
#             review.save()
#             return redirect('index')
#     return redirect('product_detail', product_id=product.id)

@login_required
def add_to_cart(request, product_id):
    # Добавление товара в корзину
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

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
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Создаем заказ
            order = Order.objects.create(
                user=request.user,
                delivery_option=form.cleaned_data['delivery_option'],
                payment_option=form.cleaned_data['payment_option'],
                status='pending'
            )

            # Добавляем товары в заказ
            for item in cart.items.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

            # Обновляем итоговую стоимость заказа
            order.update_total_price()

            # Очищаем корзину
            cart.items.all().delete()
            cart.update_total_price()

            # Редирект на страницу предварительного просмотра заказа
            return redirect('order_preview', order_id=order.id)
        else:
            return render(request, 'shop/checkout.html', {'form': form, 'cart': cart})
    else:
        form = CheckoutForm()

    return render(request, 'shop/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_preview(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if request.method == 'POST':
        delivery_option = request.POST.get('delivery_option')
        payment_option = request.POST.get('payment_option')

        if delivery_option and payment_option:
            order.delivery_option = delivery_option
            order.payment_option = payment_option
            order.update_total_price()
            order.save()

            return redirect('confirm_order', order_id=order.id)

    return render(request, 'shop/order_preview.html', {'order': order})



@login_required
def order_detail(request, order_id):
    # Получение заказа по идентификатору
    order = get_object_or_404(Order, id=order_id)

    # Отображение страницы с деталями заказа
    return render(request, 'shop/order_detail.html', {'order': order})


@login_required
def confirm_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        print("POST-запрос получен")
        print("Данные формы:", request.POST)

        # Дополнительная обработка формы здесь

        order.status = 'completed'
        order.save()

        cart = Cart.objects.get(user=request.user)
        cart.items.all().delete()

        return redirect('order_detail', order_id=order.id)
    else:
        print("Метод не POST")

    return render(request, 'shop/confirm_order.html', {'order': order})

@login_required
def confirm_logout(request):
    if request.method == 'POST':
        form = ConfirmLogoutForm(request.POST)
        if form.is_valid():
            # Проверка пароля
            user = request.user
            password = form.cleaned_data['password']
            if user.check_password(password):
                logout(request)
                return redirect('logout_done')
            else:
                form.add_error(None, 'Пароль неверен.')
    else:
        form = ConfirmLogoutForm()

    return render(request, 'shop/confirm_logout.html', {'form': form})


def create_report(order_id):
    order = get_object_or_404(Order, id=order_id)
    sales_data = {
        'items': [{'product_id': item.product.id, 'quantity': item.quantity} for item in order.items.all()],
    }

    report = Report(
        date=order.date,
        order=order,
        profit=calculate_profit(order),
        expenses=calculate_expenses(order),
        sales_data=sales_data,
    )
    report.save()

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'shop/add_review.html', {'form': form, 'product': product})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Убедитесь, что пользователь аутентифицирован
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form,
    })

def orders_report(request):
    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='completed').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()

    total_revenue = Order.objects.filter(status='completed').aggregate(Sum('total_price'))
    average_order_value = Order.objects.filter(status='completed').aggregate(Avg('total_price'))

    delivery_stats = Order.objects.values('delivery_option').annotate(count=Count('delivery_option'))
    payment_stats = Order.objects.values('payment_option').annotate(count=Count('payment_option'))

    context = {
        'total_orders': total_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'total_revenue': total_revenue['total_price__sum'],
        'average_order_value': average_order_value['total_price__avg'],
        'delivery_stats': delivery_stats,
        'payment_stats': payment_stats,
    }

    return render(request, 'shop/orders_report.html', context)

