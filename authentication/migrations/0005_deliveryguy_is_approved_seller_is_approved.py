# Generated by Django 5.1.6 on 2025-02-16 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_seller_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryguy',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='seller',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
