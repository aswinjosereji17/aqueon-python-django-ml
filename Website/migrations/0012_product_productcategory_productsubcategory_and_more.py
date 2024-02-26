# Generated by Django 4.2.3 on 2023-08-27 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Website', '0011_remove_productdescription_prod_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('prod_id', models.AutoField(primary_key=True, serialize=False)),
                ('prod_name', models.CharField(max_length=255)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ProductCategory',
            fields=[
                ('categ_id', models.AutoField(primary_key=True, serialize=False)),
                ('categ_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSubcategory',
            fields=[
                ('sub_cat_id', models.AutoField(primary_key=True, serialize=False)),
                ('sub_cat_name', models.CharField(max_length=255)),
                ('categ_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.productcategory')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDescription',
            fields=[
                ('prod_desc_id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('img1', models.ImageField(upload_to='product_images/')),
                ('img2', models.ImageField(upload_to='product_images/')),
                ('img3', models.ImageField(upload_to='product_images/')),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sub_categ_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Website.productsubcategory'),
        ),
        migrations.AddField(
            model_name='product',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]