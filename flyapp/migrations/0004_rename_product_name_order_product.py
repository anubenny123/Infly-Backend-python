# Generated by Django 3.2.19 on 2023-06-05 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flyapp', '0003_order_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product_name',
            new_name='product',
        ),
    ]
