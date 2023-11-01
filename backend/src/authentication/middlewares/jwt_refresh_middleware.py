import jwt
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from src.authentication.services import JWTService

User = get_user_model()


class JWTTokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        access_token, refresh_token = JWTService.get_tokens_from_request(request=request)

        # Если нет токенов, продолжаем как анонимный пользователь
        if not access_token:
            response = self.get_response(request)
            return response

        # Если access-токен не истек, продолжаем работу
        if not JWTService.is_expired(access_token):
            response = self.get_response(request)
            return response

        # Если refresh-токен истек, отдаем ошибку авторизации
        if JWTService.is_expired(refresh_token):
            return self.remove_tokens_and_set_error_response(request=request, error_message='Token is expired.')

        # Пробуем обновить, если access истек, а refresh нет
        try:
            refresh_token_payload = JWTService.get_payload(refresh_token)
            user_id = refresh_token_payload['user_id']
            user = User.objects.get(id=user_id)

        # Если не удалось обновить, отдаем ошибку авторизации
        except (jwt.InvalidTokenError, KeyError, User.DoesNotExist):
            return self.remove_tokens_and_set_error_response(request=request, error_message='Invalid token.')

        # Создаем новые токены
        new_access_token, new_refresh_token = JWTService.generate_tokens(user=user)

        # Даем пользователю возможность воспользоваться новыми токенами
        # для продолжения работы в текущем запросе
        request.COOKIES['access_token'] = new_access_token
        request.COOKIES['refresh_token'] = new_refresh_token

        response = self.get_response(request)

        # Устанавливаем новые токены в ответ на запрос
        response.set_cookie(key='access_token', value=new_access_token, httponly=True)
        response.set_cookie(key='refresh_token', value=new_refresh_token, httponly=True)

        return response

    def remove_tokens_and_set_error_response(self, request: Request, error_message: str) -> Response:
        request.COOKIES['access_token'] = ''
        request.COOKIES['refresh_token'] = ''
        response = self.get_response(request)
        if isinstance(response, Response):
            response.status_code = status.HTTP_401_UNAUTHORIZED
            response.data = {'error': error_message}
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            response._is_rendered = False
            response.render()

        return response
