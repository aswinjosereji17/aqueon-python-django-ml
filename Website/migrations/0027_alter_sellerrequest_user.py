# Generated by Django 4.2.3 on 2023-09-07 14:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Website', '0026_alter_productdescription_prod_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sellerrequest',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
