from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Order
from telegram_bot.tasks import send_telegram_message

@login_required
def send_orders_report(request):
    total_orders = Order.objects.count()
    completed_orders = Order.objects.filter(status='completed').count()
    cancelled_orders = Order.objects.filter(status='cancelled').count()

    report = (
        f"Отчет по заказам:\n"
        f"Всего заказов: {total_orders}\n"
        f"Завершенные заказы: {completed_orders}\n"
        f"Отмененные заказы: {cancelled_orders}\n"
    )

    send_telegram_message(request.user, report)
    return render(request, 'telegram_bot/report_sent.html')



