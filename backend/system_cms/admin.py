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


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(OrderModel)
class OrderModelAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    fields = ['customer', 'status', 'total_price', 'order_date']
    readonly_fields = ['total_price', 'order_date']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass

