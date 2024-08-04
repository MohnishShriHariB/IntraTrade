# Generated by Django 5.0.6 on 2024-06-11 07:52

import asset.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0013_alter_item_productimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ProductImage',
            field=models.ImageField(upload_to='media/assetshare/images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']), asset.models.validate_image_size]),
        ),
    ]