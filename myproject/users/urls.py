from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from users import views

urlpatterns = [
    path('login/', views.CustomAuth.as_view(), name='token_auth'),
]
