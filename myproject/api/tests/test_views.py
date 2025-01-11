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
    user = User.objects.create_user(username="testuser", password="testpass")

    client.force_authenticate(user=user)
    return client, user


@pytest.mark.django_db
def test_get_order_list(api_client):
    client, _ = api_client

    response = client.get('/api/orders/')
    assert response.status_code == status.HTTP_200_OK

  