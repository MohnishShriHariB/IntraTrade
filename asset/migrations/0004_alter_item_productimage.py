# Generated by Django 5.0.6 on 2024-06-10 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0003_alter_item_department_alter_item_empid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='ProductImage',
            field=models.FileField(upload_to='media/assetshare/images/'),
        ),
    ]
