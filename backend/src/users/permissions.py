from rest_framework import permissions


class IsListener(permissions.BasePermission):
    """
    Пользователь - слушатель
    """

    def has_permission(self, request, view):
        return request.user.role == 'listener'


class IsArtist(permissions.BasePermission):
    """
    Пользователь - исполнитель
    """

    def has_permission(self, request, view):
        return request.user.role == 'artist'
