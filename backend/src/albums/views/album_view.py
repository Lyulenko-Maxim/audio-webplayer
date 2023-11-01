from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from src.albums.models import Album
from src.albums.serializers import AlbumWithTracksReadOnlySerializer
from src.tracks.models import Track
from src.albums.serializers import AlbumReadOnlySerializer, AlbumSerializer
from src.users.permissions import IsArtist


class AlbumView(viewsets.ModelViewSet):
    queryset = Album.objects.select_related('artist')
    permission_classes = [IsAuthenticated, IsArtist]

    def get_queryset(self):
        if self.action == 'retrieve':
            self.queryset = self.queryset.prefetch_related(
                Prefetch(lookup='tracks', queryset=Track.objects.prefetch_related('genres').order_by('position'))
            )

        queryset = super().get_queryset()
        queryset = queryset.filter(artist=self.request.user.artist)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            self.serializer_class = AlbumReadOnlySerializer

        if self.action == 'retrieve':
            self.serializer_class = AlbumWithTracksReadOnlySerializer

        if self.action in ('create', 'update', 'partial_update', 'delete'):
            self.serializer_class = AlbumSerializer

        return self.serializer_class
