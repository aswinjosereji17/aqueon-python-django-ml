# Generated by Django 4.2.3 on 2023-08-13 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0003_remove_sellerrequest_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerrequest',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]
