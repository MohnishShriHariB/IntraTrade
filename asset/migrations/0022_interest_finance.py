# Generated by Django 5.0.4 on 2024-06-15 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asset', '0021_interest_given'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='Finance',
            field=models.BooleanField(default=True),
        ),
    ]
