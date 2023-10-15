from rest_framework import serializers

from .models import CustomerModel, Product, Order


class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ['id', 'full_name', 'email', 'is_deleted']


class CustomerDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = "__all__"


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        exclude = ['is_deleted']


# Probably implement BulkDeleteSerializer in the future for Bulk Deletions

# TODO: Implement other types of serializers for Product and Order models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']


# TODO: Add 'order_date' to read-only fields

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['']
