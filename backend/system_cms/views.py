from rest_framework import generics

from . import serializers
from .models import ProductModel, CustomerModel, OrderModel


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = CustomerModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.CustomerListSerializer
        return serializers.CustomerCreateSerializer


# Retrieve, Update, DELETE!!
class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.CustomerDetailedSerializer
        elif self.request.method in ["PUT", "PATCH"]:
            return serializers.CustomerUpdateSerializer
        return serializers.CustomerDetailedSerializer


class ProductListView(generics.ListCreateAPIView):
    queryset = ProductModel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.ProductListSerializer
        return serializers.ProductDetailSerializer


# Retrieve, Update, DELETE!!
class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductModel.objects.all()
    serializer_class = serializers.ProductDetailSerializer
