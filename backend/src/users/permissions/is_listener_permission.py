from rest_framework import permissions


class IsListener(permissions.BasePermission):
    """
    Пользователь - слушатель
    """

    def has_permission(self, request, view):
        return request.user.listener
