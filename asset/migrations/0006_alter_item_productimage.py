# Generated by Django 5.0.6 on 2024-06-10 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0005_alter_item_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ProductImage',
            field=models.ImageField(upload_to='media/assetshare/images/'),
        ),
    ]
