# Generated by Django 5.0.6 on 2024-06-10 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0007_alter_item_productimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='ProductImage',
        ),
    ]
