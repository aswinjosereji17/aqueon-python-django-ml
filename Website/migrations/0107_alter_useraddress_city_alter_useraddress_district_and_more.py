# Generated by Django 4.2.6 on 2024-03-25 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0106_alter_useraddress_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddress',
            name='city',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='district',
            field=models.CharField(default='', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='house_name',
            field=models.CharField(default='', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='useraddress',
            name='pincode',
            field=models.CharField(default='', max_length=10, null=True),
        ),
    ]