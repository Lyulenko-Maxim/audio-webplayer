from rest_framework.permissions import BasePermission


class IsAnonymous(BasePermission):
    """
    Пользователь - аноним
    """

    def has_permission(self, request, view):
        return request.user and not request.user.is_authenticated
