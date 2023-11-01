from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from shared.helpers import shift_positions
from src.playlists.models import PlaylistTrack
from src.playlists.serializers import PlaylistTrackSerializer
from src.playlists.permissions import IsOwnerOrReadOnlyIfPublic


class PlaylistTrackView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    queryset = PlaylistTrack.objects
    serializer_class = PlaylistTrackSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyIfPublic]

    def perform_create(self, serializer):
        total_tracks = serializer.validated_data['playlist'].tracks.count()
        serializer.validated_data['position'] = total_tracks + 1 if total_tracks != 0 else 0
        serializer.save()

    def perform_update(self, serializer):
        shift_positions(instance=serializer.instance, new_position=serializer.validated_data['position'])
        serializer.save()

    def perform_destroy(self, instance):
        shift_positions(instance=instance)
        instance.delete()
