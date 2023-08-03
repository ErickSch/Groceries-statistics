from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# erick
# lionelerick54@hotmail.com
# Pass

class Store(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=30)
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to="images")

    def __str__(self):
        return self.name


class List(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    receipt_image = models.ImageField(upload_to="images", default='')
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    total = models.FloatField()

    def __str__(self):
        return self.date


class Unit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True)
    unit = models.CharField(max_length=5)
    convert_to_int_sys = models.FloatField()

    def __str__(self):
        return self.unit


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True)
    product_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="images", default='')
    brand = models.CharField(max_length=30, default='')
    product_name_w_brand = models.CharField(max_length=40)

    def __str__(self):
        return self.product_name_w_brand


class ProductWPrice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.FloatField()
    list = models.ForeignKey(List, on_delete=models.CASCADE)
    is_preview = models.BooleanField(default=True)
    amount = models.FloatField()
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, default='')
    unit_price = models.FloatField()

    def __str__(self):
        return self.product.product_name





