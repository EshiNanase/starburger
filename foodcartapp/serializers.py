from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):

    products = serializers.ListField(
        child=OrderItemSerializer()
    )

    class Meta:
        model = Order
        fields = '__all__'
