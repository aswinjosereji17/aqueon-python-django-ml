# Generated by Django 4.2.6 on 2024-03-14 04:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Website', '0090_add_aquascape'),
    ]

    operations = [
        migrations.RenameField(
            model_name='add_aquascape',
            old_name='sub_image',
            new_name='aqsp_image',
        ),
    ]