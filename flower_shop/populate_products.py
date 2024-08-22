import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from shop.models import Product

images = [
    'products/flower1.jpg',
    'products/flower2.jpg',
    'products/flower3.jpg',
    'products/flower4.jpg',
    'products/flower5.jpg',
    'products/flower6.jpg',
    'products/flower7.jpg',
    'products/flower8.jpg',
    'products/flower9.jpg',
    'products/flower10.jpg',
]

names = [
    'Rose Bouquet',
    'Tulip Bouquet',
    'Lily Bouquet',
    'Sunflower Bouquet',
    'Daisy Bouquet',
    'Orchid Bouquet',
    'Carnation Bouquet',
    'Peony Bouquet',
    'Chrysanthemum Bouquet',
    'Lavender Bouquet',
]

prices = [
    2900.00,
    1900.00,
    2400.00,
    3400.00,
    1400.00,
    3900.00,
    1800.00,
    2500.00,
    2200.00,
    3000.00,
]

for i in range(10):
    product = Product(
        name=names[i],
        price=prices[i],
        image=images[i]
    )
    product.save()

print("Products have been added to the database.")
