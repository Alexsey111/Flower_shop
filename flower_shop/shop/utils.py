def calculate_profit(order):
    total_price = sum(item.product.price * item.quantity for item in order.items.all())
    return total_price * 0.1  # Например, 10% прибыли

def calculate_expenses(order):
    return sum(item.product.cost * item.quantity for item in order.items.all())
