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
    products = OrderProductSerializer(many=True, source='order_products')
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ['order_id', 'user', 'status', 'products', 'total_price', 'is_deleted']

    def create(self, validated_data):
        products = validated_data.pop('order_products')
        user = self.context['request'].user

        order = Order.objects.create(user=user, **validated_data)

        for product in products:
            OrderProduct.objects.create(
                order=order,
                product=product['product'],
                quantity=product['quantity']
            )

        return order
