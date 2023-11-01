from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from src.authentication.permissions import IsAnonymous
from src.authentication.services import JWTService
from src.authentication.serializers import SignInSerializer

User = get_user_model()


class SignInView(generics.GenericAPIView):
    serializer_class = SignInSerializer
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.pop('password')

        user = self.check_credentials(username=username, password=password)

        access_token, refresh_token = JWTService.generate_tokens(user)
        response = Response(data=serializer.validated_data, status=status.HTTP_200_OK)
        response = self.set_token_cookies(response, access_token, refresh_token)
        return response

    @staticmethod
    def check_credentials(username, password):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed('Неверный логин или пароль')

        if not user.check_password(raw_password=password):
            raise AuthenticationFailed('Неверный логин или пароль')

        return user

    @staticmethod
    def set_token_cookies(response, access_token, refresh_token):
        response.set_cookie(
            key='access_token',
            value=access_token,
            httponly=True,
        )
        response.set_cookie(
            key='refresh_token',
            value=refresh_token,
            httponly=True
        )
        return response
