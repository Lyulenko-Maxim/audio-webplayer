from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.playlists.models import PlaylistTrack
from src.playlists.models.playlist import Playlist
from src.playlists.serializers import PlaylistReadOnlySerializer, PlaylistSerializer, \
    PlaylistTrackSerializer, PlaylistWithTracksReadOnlySerializer
from src.playlists.permissions import IsOwnerOrReadOnlyIfPublic
from src.tracks.serializers import TrackSerializer


class PlaylistReadOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Playlist.objects
        .prefetch_related('tracks')
        .filter(is_public=True)
    )
    serializer_class = PlaylistReadOnlySerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     self.queryset = Playlist.objects.filter(user=self.request.user)
    #     return self.queryset

    # def get_permissions(self):
    #     if self.action in ('list', 'retrieve'):
    #         self.permission_classes = [IsOwnerOrReadOnlyIfPublic]
    #
    #     if self.action in ('create', 'update', 'partial_update', 'delete'):
    #         self.permission_classes = [IsAuthenticated, IsOwnerOrReadOnlyIfPublic]
    #
    #     return [permission() for permission in self.permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = PlaylistReadOnlySerializer

        if self.action == 'retrieve':
            self.serializer_class = PlaylistWithTracksReadOnlySerializer

        # if self.action in ('create', 'update', 'partial_update', 'delete'):
        #     self.serializer_class = PlaylistSerializer

        return self.serializer_class

    # @action(detail=True, methods=['post'], url_path='add-track', serializer_class=PlaylistTrackSerializer)
    # def add_track(self, request, pk=None):
    #     playlist = get_object_or_404(Playlist, user=request.user, pk=pk)
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     playlist_track = PlaylistTrack(
    #         playlist=playlist,
    #         track=serializer.validated_data['track'],
    #         position=serializer.validated_data['position']
    #     )
    #     playlist_track.save()
    #     return Response({'трек добавлен'})
