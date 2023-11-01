import jwt
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import Request

from src.authentication.services import JWTService

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    Аутентификация через JWT-токены.
    """

    def authenticate(self, request: Request) -> tuple[User, None] | None:
        access_token, _ = JWTService.get_tokens_from_request(request=request)

        # Если нет токена, продолжаем работу как анонимный пользователь
        if not access_token:
            return None

        # Пробуем получить пользователя из токена
        try:
            payload = JWTService.get_payload(access_token)
            user_id = payload['user_id']
            username = payload['username']
            user = User.objects.get(pk=user_id, username=username)
            return user, None

        # Если не удалось получить пользователя из токена,
        # продолжаем работу как анонимный пользователь
        except (jwt.DecodeError, KeyError, User.DoesNotExist):
            return None
