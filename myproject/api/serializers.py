from rest_framework import serializers

from api.models import Order, Product, OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["product_id", "name", "price"]


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, source='orderproduct_set', read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'user', 'status', 'total_price', 'products', 'is_deleted']

