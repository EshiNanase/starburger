from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):

    products = serializers.ListField(
        child=OrderItemSerializer(),
        allow_empty=False,
        write_only=True
    )

    class Meta:
        model = Order
        fields = '__all__'

    def save(self, **kwargs):
        order = Order.objects.create(
            firstname=self.validated_data['firstname'],
            lastname=self.validated_data['lastname'],
            phonenumber=self.validated_data['phonenumber'],
            address=self.validated_data['address'],
        )
        return order
