from pprint import pprint

from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from src.oauth.services import JWTService
from src.oauth.serializers import UserSerializer

User = get_user_model()


class RegisterView(APIView):
    """
    Представление для регистрации пользователя.
    """

    @staticmethod
    def post(request: Request) -> Response:
        serializer = UserSerializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response(data = serializer.data, status = status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    Представление для авторизации пользователя.
    """

    @staticmethod
    def post(request: Request) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username = username)

        except User.DoesNotExist:
            user = None

        if user is None or not user.check_password(raw_password = password):
            raise AuthenticationFailed('Неверный логин или пароль')

        access_token, refresh_token = JWTService.generate_tokens(user)

        response = Response(data = {
            'message': 'Успешный вход!'
        })

        response.set_cookie(
            key = 'access_token',
            value = access_token,
            httponly = True
        )

        response.set_cookie(
            key = 'refresh_token',
            value = refresh_token,
            httponly = True
        )

        return response


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
