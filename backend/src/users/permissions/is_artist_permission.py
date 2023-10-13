from rest_framework import permissions


class IsArtist(permissions.BasePermission):
    """
    Пользователь - исполнитель
    """

    def has_permission(self, request, view):
        return request.user.artist
