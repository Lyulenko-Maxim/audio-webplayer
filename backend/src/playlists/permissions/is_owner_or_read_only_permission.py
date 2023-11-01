from rest_framework import permissions


class IsOwnerOrReadOnlyIfPublic(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and hasattr(obj, 'is_public') and obj.is_public:
            return True

        if hasattr(obj, 'playlist'):
            return obj.playlist.user == request.user

        if hasattr(obj, 'user'):
            return obj.user == request.user

        return False
