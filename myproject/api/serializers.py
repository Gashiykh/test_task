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

    def update(self, instance, validated_data):
        products = validated_data.pop('order_products', None)

        instance.status = validated_data.get('status', instance.status)
        instance.save()

        if products:
            for product in products:
                product_id = product['product'].product_id
                quantity = product['quantity']

                order = instance.order_products.filter(product_id=product_id).first()

                if order:
                    order.quantity = quantity
                    order.save()
                else:
                    raise serializers.ValidationError(
                    {"detail": f"Продукт с id {product_id} не существует в заказе."}
                    )
            
        return instance