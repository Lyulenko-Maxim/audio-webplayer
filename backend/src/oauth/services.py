from datetime import datetime, timedelta

import jwt
from rest_framework.request import Request

from config.settings import SECRET_KEY
from src.users.models import User


class JWTService:
    @staticmethod
    def generate_tokens(user: User) -> tuple[str | bytes, str | bytes]:
        """
        Генерирует access token и refresh токены для заданного пользователя.
        """

        access_token_payload = {
            'user_id': user.id,
            'username': user.username,
            'iat': datetime.timestamp(datetime.now()),
            'exp': datetime.utcnow() + timedelta(minutes = 5),
        }

        refresh_token_payload = {
            'user_id': user.id,
            'username': user.username,
            'iat': datetime.timestamp(datetime.now()),
            'exp': datetime.utcnow() + timedelta(days = 7),
        }

        access_token = jwt.encode(
            payload = access_token_payload,
            key = SECRET_KEY,
            algorithm = 'HS256',
            headers = {'typ': 'JWT', },
        )

        refresh_token = jwt.encode(
            payload = refresh_token_payload,
            key = SECRET_KEY,
            algorithm = 'HS256',
            headers = {'typ': 'JWT', },
        )
        return access_token, refresh_token

    @staticmethod
    def get_tokens_from_request(request: Request) -> tuple[str, str] | tuple[None, None]:
        """
        Получает access и refresh токены из запроса.
        """

        try:
            access_token = request.COOKIES['access_token']
            refresh_token = request.COOKIES['refresh_token']
            return access_token, refresh_token

        except KeyError:
            return None, None

    @staticmethod
    def is_expired(token: str | bytes) -> bool:
        """
        Проверяет, истек ли токен.
        """

        try:
            JWTService.get_payload(token = token)
            return False

        except jwt.ExpiredSignatureError:
            return True

    @staticmethod
    def get_payload(token: str | bytes) -> dict:
        """
        Декодирует payload у токена.
        """

        payload = jwt.decode(
            jwt = token,
            key = SECRET_KEY,
            algorithms = ['HS256']
        )

        return payload
