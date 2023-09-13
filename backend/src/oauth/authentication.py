import jwt
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from src.oauth.services import JWTService

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    """
    Аутентификация через JWT-токены.
    """

    def authenticate(self, request: Request) -> tuple[User, None] | None:
        access_token, _ = JWTService.get_tokens_from_request(request = request)

        # Если нет хотя бы одного токена, продолжаем работу как неавторизованный пользователь
        if not access_token:
            return None

        try:
            payload = JWTService.get_payload(access_token)
            user_id = payload.get('user_id')
            user = User.objects.get(pk = user_id)
            return user, None

        except AuthenticationFailed:
            return None
