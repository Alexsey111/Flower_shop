import os
import sys
from flower_shop.shop.models import Order

# Добавляем путь к корневой папке проекта в sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flower_shop.settings')
django.setup()

def generate_order_report():
    # Получаем все заказы
    orders = Order.objects.all()

    # Пример анализа
    total_sales = sum(order.total_price for order in orders)
    total_orders = orders.count()

    return {
        'total_sales': total_sales,
        'total_orders': total_orders,
    }

# Пример использования функции
if __name__ == "__main__":
    report = generate_order_report()
    print(report)
