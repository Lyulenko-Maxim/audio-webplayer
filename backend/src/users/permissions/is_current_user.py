from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsCurrentUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user

        return obj == request.user
