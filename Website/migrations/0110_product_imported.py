# Generated by Django 4.2.6 on 2024-03-31 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0109_order_serial_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imported',
            field=models.BooleanField(default=False),
        ),
    ]