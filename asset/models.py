from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

def validate_image_size(image):
    max_size = 1024 * 1024
    if image.size > max_size:
        raise ValidationError('The image size should not exceed 1MB.')

class Item(models.Model):
    EmpID = models.CharField(max_length=255)
    EmpName = models.CharField(max_length=255)
    Department = models.CharField(max_length=255)
    MobileNo = models.BigIntegerField()
    ProductName = models.CharField(max_length=255)
    ProductType = models.CharField(max_length=255)
    FinanceType = models.CharField(max_length=255)
    ProductDesc = models.TextField(max_length=255)
    ProductCount = models.BigIntegerField()
    ProductImage = models.ImageField(
        upload_to="media/assetshare/images/",
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif']),
            validate_image_size,
        ]
    )
    Approved = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.ProductName

class Interest(models.Model):
    Item_id = models.ForeignKey(Item, on_delete=models.CASCADE, db_index=True)
    EmpID = models.CharField(max_length=100)
    Department = models.CharField(max_length=150)
    MobileNo = models.BigIntegerField()
    Product_count = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    Approved = models.BooleanField(default=False)
    Given = models.BooleanField(default=False)
    Finance = models.BooleanField(default=True)
    valid = models.BooleanField(default=True)


class Hod(models.Model):
    hod_id = models.CharField(max_length=100)
    hod_password = models.CharField(max_length=100)
    Department = models.CharField(max_length=150)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        user, created = User.objects.get_or_create(username=self.hod_id)
        user.set_password(self.hod_password)
        user.save()

class BandF(models.Model):
    BF_id = models.CharField(max_length=100)
    BF_password = models.CharField(max_length=100)


class product_types(models.Model):
    type=models.CharField(max_length=200)

    def __str__(self):
        return self.type
    
class Product(models.Model):
    name = models.CharField(max_length=100)
    product_type = models.ForeignKey(product_types, on_delete=models.CASCADE)

    def __str__(self):
        return self.name