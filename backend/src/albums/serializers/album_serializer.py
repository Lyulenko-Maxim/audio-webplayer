from rest_framework import serializers

from shared.serializers import CurrentArtistDefault
from src.albums.models import Album


class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.HiddenField(default=CurrentArtistDefault())

    class Meta:
        model = Album
        fields = ('id', 'type', 'title', 'description', 'release', 'cover', 'artist')
