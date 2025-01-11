import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.shortcuts import get_object_or_404
from django.db.models import Sum, F
from django.core.cache import cache

from api.models import (
    Order,
    Product,
    OrderProduct
    )
from api.serializers import (
    OrderSerializer,
    ProductSerializer, 
    OrderProductSerializer
    ) 

logger = logging.getLogger('user_actions')

class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):

        if 'id' in kwargs:

            order_id = kwargs['id']  
            cache_key = f"order_{order_id}" 
            order_data = cache.get(cache_key)

            if order_data:
                logger.info(f"Данные заказа с ID {order_id} получены из кэша")
                return Response(order_data, status=status.HTTP_200_OK)

            order = get_object_or_404(
                Order,
                order_id=order_id,
                is_deleted=False
            )

            if order.user != request.user and not request.user.is_superuser:
                logger.info(f"У пользователя {request.user.username} нет прав на просмотр заказа с ID {order_id}")
                return Response(
                    {"detail": "Нет прав на просмотр этого заказа."},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = OrderSerializer(order)
            cache.set(cache_key, serializer.data, timeout=300)
            logger.info(f"Данные заказа с ID {order.order_id} добавлены в кэш для ключа {cache_key}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            status_filter = request.query_params.get('status')
            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')

            queryset = Order.objects.filter(is_deleted=False)

            queryset = queryset.annotate(
            total_price=Sum(F('order_products__product__price') * F('order_products__quantity'))
            )

            if status_filter:
                queryset = queryset.filter(status=status_filter)
            if min_price:
                queryset = queryset.filter(total_price__gte=min_price)
            if max_price:
                queryset = queryset.filter(total_price__lte=max_price)

            serializer = OrderSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):

        serializer = OrderSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            order = serializer.save()

            cache_key = f"order_{order.order_id}"
            cache.set(cache_key, serializer.data, timeout=300)
            logger.info(f"Данные заказа с ID {order.order_id} добавлены в кэш для ключа {cache_key}")

            logger.info(f"Пользователь {request.user.username} создал заказ с ID {order.order_id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Ошибка при создании заказа пользователем {request.user.username}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):

        order_id = kwargs['id']

        order = get_object_or_404(
            Order,
            order_id=kwargs['id'],
            is_deleted=False
        )
        if order.user != request.user and not request.user.is_superuser:
            logger.info(f"У пользователя {request.user.username} нет прав на редактирование заказа с ID {order.order_id}")
            return Response(
                {"detail": "Нет прав на редактирование этого заказа."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = OrderSerializer(
            order,
            data=request.data,
            partial=True,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            cache_key = f"order_{order_id}"
            cache.set(cache_key, serializer.data, timeout=300)
            logger.info(f"Данные заказа с ID {order.order_id} добавлены в кэш для ключа {cache_key}")
            logger.info(f"Пользователь {request.user.username} обновил заказ с ID {order.order_id}")
            return Response(serializer.data)
        logger.warning(f"Ошибка при обновлении заказа с ID {order_id} пользователем {request.user.username}: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):

        order_id = kwargs['id']

        order = get_object_or_404(
            Order,
            order_id=kwargs['id'],
            is_deleted=False
        )

        if order.user != request.user and not request.user.is_superuser:
            logger.info(f"У пользователя {request.user.username} нет прав на удаление заказа с ID {order.order_id}")
            return Response(
                {"detail": "Нет прав на удаление этого заказа."},
                status=status.HTTP_403_FORBIDDEN
            )
        order.is_deleted = True
        order.save()

        cache_key = f"order_{order_id}"
        cache.delete(cache_key)

        logger.info(f"Пользователь {request.user.username} удалил заказ с ID {order_id} из базы и кэша")
        return Response(
            {"detail": f"Заказ {kwargs['id']} успешно удален."},
            status=status.HTTP_204_NO_CONTENT
        )