from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.shortcuts import get_object_or_404

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


class OrderView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):

        if 'id' in kwargs:
            order = get_object_or_404(
                Order,
                id=kwargs['id'],
                is_deleted=False
            )

            if order.user != request.user and not request.user.is_superuser:
                return Response(
                    {"detail": "Нет прав на просмотр этого заказа."},
                    status=status.HTTP_403_FORBIDDEN
                )
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            status_filter = request.query_params.get('status')

            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')

            queryset = Order.objects.filter(is_deleted=False)

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
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
