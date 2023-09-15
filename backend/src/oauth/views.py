from django.contrib.auth import get_user_model
from rest_framework import generics, serializers, status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from oauth.permissions import IsAnonymous
from src.oauth.services import JWTService
from src.oauth.serializers import ArtistSerializer, ListenerSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Представление для регистрации пользователя.
    """

    serializer_class = UserSerializer
    permission_classes = [IsAnonymous]

    def perform_create(self, serializer):
        user_data = self.request.data.copy()
        user = serializer.save()
        role = self.request.data.get('role')
        user_data['user'] = user.id

        if role == 'listener':
            listener_serializer = ListenerSerializer(data = user_data)
            if not listener_serializer.is_valid():
                user.delete()
                raise serializers.ValidationError(listener_serializer.errors)

            listener_serializer.save()
            return

        if role == 'artist':
            artist_serializer = ArtistSerializer(data = user_data)

            if not artist_serializer.is_valid():
                user.delete()
                raise serializers.ValidationError(artist_serializer.errors)

            artist_serializer.save()
            return

        raise serializers.ValidationError(
            detail = "Неподдерживаемая роль",
            code = status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):
    """
    Представление для авторизации пользователя.
    """

    @staticmethod
    def post(request: Request, *args, **kwargs) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username = username)

        except User.DoesNotExist:
            user = None

        if user is None or not user.check_password(raw_password = password):
            raise AuthenticationFailed('Неверный логин или пароль')

        access_token, refresh_token = JWTService.generate_tokens(user)

        response = Response(
            data = {'message': 'Успешный вход!'},
            status = status.HTTP_200_OK
        )

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
