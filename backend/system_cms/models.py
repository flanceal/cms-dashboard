from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    last_login = models.DateTimeField(auto_now=True, null=False, blank=True)
    is_staff = models.BooleanField(null=False, blank=True)
    is_superuser = models.BooleanField(null=False, blank=True)

    # emai is as username here and main identifier
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()


class CustomerModel(models.Model):
    full_name = models.CharField(max_length=110, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    phone_number = PhoneNumberField(unique=True, blank=True)
    address = models.CharField(blank=True, max_length=300)
    is_deleted = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return self.full_name


class Product(models.Model):
    name = models.CharField(max_length=175, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    stock = models.PositiveIntegerField(default=0, null=True, blank=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(CustomerModel, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product, through='OrderItem')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    order_date = models.DateTimeField(auto_now_add=True, null=False, blank=True)

    def __str__(self):
        return f"Order #{self.id}"

    def calculate_total_price(self):
        total = sum([item.quantity * item.product.price for item in self.orderitem_set.all()])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

