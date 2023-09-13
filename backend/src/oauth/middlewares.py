import jwt
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect, JsonResponse
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response

from src.oauth.services import JWTService

User = get_user_model()


class TokenRefreshMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: Request):
        access_token, refresh_token = JWTService.get_tokens_from_request(request = request)

        # Если нет хотя бы одного токена, продолжаем работу как неавторизованный пользователь
        if not access_token or not refresh_token:
            response = self.get_response(request)
            return response

        # Если access не истек, продолжаем работу
        if not JWTService.is_expired(access_token):
            response = self.get_response(request)
            return response

        # Если access и refresh истекли, прерываем работу и отдаем HTTP_401_UNAUTHORIZED
        if JWTService.is_expired(refresh_token):
            return JsonResponse(
                data = {'error': 'Unauthorized'},
                status = status.HTTP_401_UNAUTHORIZED
            )

        try:
            refresh_token_payload = JWTService.get_payload(refresh_token)
            user_id = refresh_token_payload['user_id']
            user = User.objects.get(id = user_id)

        except (jwt.InvalidTokenError, KeyError, User.DoesNotExist):
            return JsonResponse(
                data = {'error': 'Unauthorized'},
                status = status.HTTP_401_UNAUTHORIZED
            )

        new_access_token, new_refresh_token = JWTService.generate_tokens(user = user)

        request.COOKIES['access_token'] = new_access_token
        request.COOKIES['refresh_token'] = new_refresh_token

        response = self.get_response(request)

        response.set_cookie(
            key = 'access_token',
            value = new_access_token,
            httponly = True
        )

        response.set_cookie(
            key = 'refresh_token',
            value = new_refresh_token,
            httponly = True
        )

        return response
