from django.contrib import admin

from .models import CustomUserModel, CustomerModel, ProductModel, OrderModel, OrderItem


@admin.register(CustomUserModel)
class CustomUserModelAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerModel)
class CustomerModelAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductModel)
class ProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass
