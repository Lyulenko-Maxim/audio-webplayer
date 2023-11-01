from rest_framework import serializers

from src.albums.serializers import AlbumReadOnlySerializer
from src.artists.serializers import ArtistReadOnlySerializer
from src.tracks.serializers import TrackReadOnlySerializer


class SearchReadOnlySerializer(serializers.Serializer):
    albums = AlbumReadOnlySerializer(many=True, read_only=True)
    tracks = TrackReadOnlySerializer(many=True, read_only=True)
    artists = ArtistReadOnlySerializer(many=True, read_only=True)
