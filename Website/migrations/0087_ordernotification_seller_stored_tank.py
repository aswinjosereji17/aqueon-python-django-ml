# Generated by Django 4.2.6 on 2024-02-28 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0086_order_all_received'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordernotification_seller',
            name='stored_tank',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
    ]
