from django.contrib import admin
from django.urls import path
from rest_framework import routers

from api import views

urlpatterns = [
    path('orders/', views.OrderView.as_view(), name='order_list_create'),
    path('orders/<int:id>/', views.OrderView.as_view(), name='order_detail'),
]