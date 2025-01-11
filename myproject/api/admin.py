from django.contrib import admin
from api.models import (
    Product,
    Order,
    OrderProduct
)
from users.models import User

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderProduct)