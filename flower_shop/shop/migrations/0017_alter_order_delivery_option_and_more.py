# Generated by Django 5.1 on 2024-08-22 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0016_alter_review_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_option',
            field=models.CharField(choices=[('standard', 'Standard Delivery'), ('express', 'Express Delivery'), ('pickup', 'Pickup')], default='standard', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_option',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal'), ('cash_on_delivery', 'Cash on Delivery')], default='credit_card', max_length=20),
        ),
    ]
