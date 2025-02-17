# Generated by Django 5.0.6 on 2024-06-10 10:54

import asset.models
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0010_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ProductImage',
            field=models.ImageField(upload_to='media/assetshare/images/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']), asset.models.validate_image_size]),
        ),
    ]
