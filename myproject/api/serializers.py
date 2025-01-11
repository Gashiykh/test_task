from rest_framework import serializers

from api.models import Order, Product, OrderProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["product_id", "name", "price"]


class OrderProductSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['product_id', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, source='order_products', read_only=True)
    new_products = OrderProductSerializer(many=True, write_only=True) 

    class Meta:
        model = Order
        fields = ['order_id', 'user', 'status', 'products', 'new_products', 'is_deleted']

