from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'order']

    def create(self, validated_data):
        validated_data['cost'] = validated_data['product'].price
        return OrderItem.objects.create(**validated_data)


class OrderSerializer(serializers.ModelSerializer):

    products = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['products', 'firstname', 'lastname', 'phonenumber', 'address']

    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product in products:
            product['order'] = order.id
            serializer = OrderItemSerializer(data=product)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return order
