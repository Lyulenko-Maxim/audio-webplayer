from src.albums.models import Album
from src.artists.serializers import ArtistSerializer
from shared.serializers import ReadOnlyModelSerializer


class AlbumReadOnlySerializer(ReadOnlyModelSerializer):
    artist = ArtistSerializer()

    class Meta:
        model = Album
        fields = ('id', 'type', 'title', 'description', 'release', 'cover', 'artist',)
