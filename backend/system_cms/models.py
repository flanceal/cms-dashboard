from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    last_login = models.DateTimeField(auto_now=True, null=False, blank=True)
    is_staff = models.BooleanField(null=False, blank=False, default=False)
    is_superuser = models.BooleanField(null=False, blank=False, default=False)

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


class ProductModel(models.Model):
    name = models.CharField(max_length=175, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    stock = models.PositiveIntegerField(default=0, null=True, blank=False)

    def __str__(self):
        return self.name


class OrderModel(models.Model):
    ORDER_STATUSES = (
        ('created', 'CREATED'),
        ('delivering', 'DELIVERING'),
        ('completed', 'COMPLETED')
    )

    customer = models.ForeignKey(CustomerModel, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(ProductModel, through='OrderItem', null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    order_date = models.DateTimeField(auto_now_add=True, null=False, blank=True)
    status = models.CharField(max_length=11, choices=ORDER_STATUSES, default='created')

    def __str__(self):
        return f"Order #{self.id}"

    def delete(self, using=None, keep_parents=False):
        if self.status != 'created':
            raise ValidationError('Order can not be deleted if it is being Delivered or is Completed')
        super().delete(using=using, keep_parents=keep_parents)


class OrderItem(models.Model):
    order = models.ForeignKey(OrderModel, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        super(OrderItem, self).save(*args, **kwargs)  # Save the OrderItem first
        self.update_order_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super(OrderItem, self).delete(*args, **kwargs)
        order.refresh_from_db()
        order.save()  # This will trigger the re-calculation of total

    def update_order_total(self):
        total = sum([item.quantity * item.product.price for item in self.order.orderitem_set.all()])
        self.order.total_price = total
        self.order.save()


@receiver(pre_delete, sender=OrderModel)
def prevent_bulk_delete(sender, instance, **kwargs):
    # Checks order's status to be 'created' before every delete and bulk delete, otherwise raises an error
    if instance.status != 'created':
        raise ValidationError('Order cannot be deleted if it is being Delivered or is Completed')
