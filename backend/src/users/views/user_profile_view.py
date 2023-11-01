from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from src.users.permissions import IsCurrentUser
from src.users.serializers import ChangePasswordSerializer, UserProfileSerializer, UserSerializer

User = get_user_model()


class UserProfileView(GenericViewSet):
    queryset = User.objects.select_related('profile')
    permission_classes = [IsAuthenticated, IsCurrentUser]
    serializer_class = UserSerializer

    def list(self, request):
        user = self.queryset.get(id=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], url_path='edit', serializer_class=UserProfileSerializer)
    def update_profile(self, request):
        profile = request.user.profile
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Профиль успешно изменен'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], url_path='account/edit', serializer_class=UserSerializer)
    def update_account(self, request):
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Профиль успешно изменен'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['put'], serializer_class=ChangePasswordSerializer, url_path='change-password')
    def change_password(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        user.set_password(serializer.validated_data.get('new_password'))
        user.save()
        return Response({'message': 'Пароль успешно изменен'}, status=status.HTTP_200_OK)
