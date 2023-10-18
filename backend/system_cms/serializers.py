from rest_framework import serializers

from .models import CustomerModel, ProductModel, OrderModel, OrderItem


# For showing all the customers
class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ['id', 'full_name', 'email', 'is_deleted']
        read_only_fields = ['__all__']


# show specific customer data
class CustomerDetailedSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = "__all__"


class CustomerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        exclude = ['is_deleted']


class CustomerUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        exclude = ['email']


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        exclude = ['description']
        read_only_fields = ['__all__']


# for showing specific product data, creating or updating product
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    customer_fullname = serializers.SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = ['id', 'customer_fullname', 'total_price', 'order_date', 'status']
        read_only_fields = ['__all__']

    def get_customer_fullname(self, obj):
        if obj.customer:
            return obj.customer.full_name
        return None


class OrderItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemCreateSerializer(source='orderitem_set', many=True)

    class Meta:
        model = OrderModel
        fields = ['customer', 'items', 'status']

    def create(self, validated_data):
        items_data = validated_data.pop('orderitem_set')
        order = OrderModel.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order


class OrderDetailSerializer(serializers.ModelSerializer):
    customer_fullname = serializers.SerializerMethodField()
    customer_id = serializers.SerializerMethodField()
    items = OrderItemCreateSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = OrderModel
        fields = ['customer_fullname', 'customer_id', 'items', 'total_price', 'order_date', 'status']
        read_only_fields = ['items', 'total_price', 'order_date']

    def get_customer_fullname(self, obj):
        if obj.customer:
            return obj.customer.full_name
        return None

    def get_customer_id(self, obj):
        if obj.customer:
            return obj.customer.id
        return None
