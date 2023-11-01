from src.albums.models import Album
from src.artists.serializers import ArtistReadOnlySerializer
from shared.serializers import ReadOnlyModelSerializer
from src.tracks.serializers import TrackInAlbumReadOnlySerializer


class AlbumWithTracksReadOnlySerializer(ReadOnlyModelSerializer):
    artist = ArtistReadOnlySerializer()
    tracks = TrackInAlbumReadOnlySerializer(many=True)

    class Meta:
        model = Album
        fields = ('id', 'type', 'title', 'description', 'release', 'cover', 'artist', 'tracks')
