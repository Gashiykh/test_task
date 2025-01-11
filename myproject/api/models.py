from django.db import models
from django.contrib.auth import get_user_model


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, verbose_name="Название продукта")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость продукта")

    def __str__(self):
        return self.name
    

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    order_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), related_name="orders", on_delete=models.CASCADE, verbose_name="Клиент")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Статус заказа")
    products = models.ManyToManyField(Product, through='OrderProduct', related_name='orders', verbose_name="Продукты")
    is_deleted = models.BooleanField(default=False, verbose_name="Удалён")

    def total_price(self):
        total = 0
        for item in self.order_product.all():
            price = item.product.price
            quantity = item.quantity
            item_total = price * quantity
            total += item_total
        return round(total, 2)

    def __str__(self):
        return f"Заказ {self.order_id} от {self.user.username}"


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name="Количество продукта в заказе")

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'