# Generated by Django 4.2 on 2025-02-20 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0017_order_delivery_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryaddress',
            name='address',
            field=models.CharField(max_length=500),
        ),
    ]
