# Generated by Django 4.2.3 on 2023-08-27 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0010_product_productcategory_productsubcategory_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productdescription',
            name='prod_id',
        ),
        migrations.RemoveField(
            model_name='productsubcategory',
            name='categ_id',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
        migrations.DeleteModel(
            name='ProductCategory',
        ),
        migrations.DeleteModel(
            name='ProductDescription',
        ),
        migrations.DeleteModel(
            name='ProductSubcategory',
        ),
    ]
