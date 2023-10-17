from rest_framework import serializers

from .models import CustomerModel, ProductModel, OrderModel, OrderItem


# For showing all the customers
class CustomerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = ['id', 'full_name', 'email', 'is_deleted']
        read_only_fields = '__all__'


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
        read_only_fields = '__all__'


# for showing specific product data, creating or updating product
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = '__all__'


class OrderListSerializer(serializers.ModelSerializer):
    customer_fullname = serializers.SerializerMethodField()

    class Meta:
        model = OrderModel
        fields = ['id', 'customer_fullname', 'total_price', 'order_date']
        read_only_fields = '__all__'

    def get_customer_fullname(self, obj):
        if obj.customer:
            return obj.customer.full_name
        return None


class ProductIdAndNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductModel
        fields = ['id', 'name']


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductIdAndNameSerializer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderDetailSerializer(serializers.ModelSerializer):
    customer_fullname = serializers.SerializerMethodField()
    items = OrderItemSerializer(source='orderitem_set', many=True)

    class Meta:
        model = OrderModel
        fields = ['id', 'customer_fullname', 'items', 'total_price', 'order_date', 'status']

    def get_customer_fullname(self, obj):
        if obj.customer:
            return obj.customer.full_name
        return None


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderModel
        exclude = ['total_price', 'order_date']