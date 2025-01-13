import pytest
from rest_framework.test import APIClient
from rest_framework import status
from django.core.cache import cache

from django.contrib.auth import get_user_model

from api.models import Product, Order, OrderProduct


@pytest.fixture
def api_client():
    client = APIClient()
    
    User = get_user_model()
    user = User.objects.create_user(username="testuser", password="testpass", is_superuser=True)

    client.force_authenticate(user=user)
    return client, user


@pytest.mark.django_db
def test_get_order_list(api_client):
    client, _ = api_client

    response = client.get('/api/orders/')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_order_detail_cache(api_client):

    client, user = api_client

    product = Product.objects.create(name="Milk", price="100.00")
    order = Order.objects.create(user=user, status='pending')
    OrderProduct.objects.create(order=order, product=product, quantity=1)

    cache_key = f"order_{order.order_id}"
    cache.set(cache_key, {"order_id": order.order_id, "status": "cached"}, timeout=300)

    response = client.get(f"/api/orders/{order.order_id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "cached"


@pytest.mark.django_db
def test_get_order_db(api_client):
    
    client, user = api_client

    product = Product.objects.create(name="Milk", price="100.00")
    order = Order.objects.create(user=user, status='pending')
    OrderProduct.objects.create(order=order, product=product, quantity=1)

    cache_key = f"order_{order.order_id}"
    cache.delete(cache_key)

    response = client.get(f"/api/orders/{order.order_id}/")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "pending"


@pytest.mark.django_db
def test_post_order(api_client):
    client, user = api_client

    product = Product.objects.create(name="Bread", price="500")

    data = {
        "status": "pending",
        "products": [{
            "product_id": product.product_id, 
            "quantity": 2
        }]
    }

    response = client.post("/api/orders/", data=data, format='json')

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["status"] == "pending"
    assert response.data["products"][0]["quantity"] == 2


@pytest.mark.django_db
def test_patch_order(api_client):

    client, user = api_client

    product = Product.objects.create(name="Juice", price="300")
    order = Order.objects.create(user=user, status="pending")

    OrderProduct.objects.create(order=order, product=product, quantity=2)

    data = {
        "status": "confirmed"
    }

    response = client.patch(f"/api/orders/{order.order_id}/", data=data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["status"] == "confirmed"
  

@pytest.mark.django_db
def test_delete_order(api_client):

    client, user = api_client

    product = Product.objects.create(name="Butter", price="300")
    order = Order.objects.create(user=user, status="pending")

    OrderProduct.objects.create(order=order, product=product, quantity=1)

    response =client.delete(f"/api/orders/{order.order_id}/")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Order.objects.filter(order_id=order.order_id, is_deleted=True).exists()