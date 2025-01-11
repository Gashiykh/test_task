from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
import logging

logger = logging.getLogger('user_actions')

class CustomAuth(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = response.data.get('token')
        if token:
            logger.info(f"Пользователь {request.user.username} авторизован")
        else:
            logger.warning(f"Неудачная авторизация для пользователя {request.data.get('username')}.")
        return response
