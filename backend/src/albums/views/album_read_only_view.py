from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from src.albums.models import Album
from src.tracks.models import Track
from src.albums.serializers import AlbumReadOnlySerializer, AlbumWithTracksReadOnlySerializer


class AlbumReadOnlyView(viewsets.ReadOnlyModelViewSet):
    queryset = Album.objects.select_related('artist')
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.action == 'retrieve':
            self.queryset = self.queryset.prefetch_related(
                Prefetch(lookup='tracks', queryset=Track.objects.order_by('position'))
            )

        queryset = super().get_queryset()
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = AlbumReadOnlySerializer

        if self.action == 'retrieve':
            self.serializer_class = AlbumWithTracksReadOnlySerializer

        serializer_class = super().get_serializer_class()
        return serializer_class
