from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.albums.models import Album
from src.albums.serializers import AlbumReadOnlySerializer
from src.artists.models import Artist
from src.artists.serializers import ArtistReadOnlySerializer
from src.search.filters import AlbumFilter, ArtistFilter, TrackFilter
from src.search.serializers import SearchReadOnlySerializer, SearchSerializer
from src.tracks.models import Track
from src.tracks.serializers import TrackReadOnlySerializer


class SearchView(ListAPIView):
    serializer_class = SearchSerializer
    filter_backends = (DjangoFilterBackend,)
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        search_term = serializer.validated_data.get('q', '')
        search_artists = serializer.validated_data.get('artists', False)
        search_albums = serializer.validated_data.get('albums', False)
        search_tracks = serializer.validated_data.get('tracks', False)

        artists_data = []
        albums_data = []
        tracks_data = []

        if search_artists:
            artist_filter = ArtistFilter(request.GET, queryset=Artist.objects.filter(stage_name__icontains=search_term))
            artists_data = ArtistReadOnlySerializer(artist_filter.qs, many=True).data

        if search_albums:
            album_filter = AlbumFilter(request.GET, queryset=Album.objects.filter(title__icontains=search_term))
            albums_data = AlbumReadOnlySerializer(album_filter.qs, many=True).data

        if search_tracks:
            track_filter = TrackFilter(request.GET, queryset=Track.objects.filter(title__icontains=search_term))
            tracks_data = TrackReadOnlySerializer(track_filter.qs, many=True).data

        result_data = {
            'albums': albums_data,
            'tracks': tracks_data,
            'artists': artists_data,
        }
        return Response(result_data)
