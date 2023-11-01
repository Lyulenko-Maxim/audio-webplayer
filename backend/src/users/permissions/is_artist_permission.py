from rest_framework import permissions


class IsArtist(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_artist

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user

        if hasattr(obj, 'artist'):
            return obj.artist.user == request.user

        if hasattr(obj, 'album'):
            return obj.album.artist.user == request.user

        return False
