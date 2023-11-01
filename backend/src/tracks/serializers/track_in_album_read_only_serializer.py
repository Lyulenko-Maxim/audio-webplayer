from src.artists.serializers import ArtistReadOnlySerializer
from src.genres.serializers.genre_serializer import GenreSerializer
from src.tracks.models import Track
from shared.serializers import ReadOnlyModelSerializer


class TrackInAlbumReadOnlySerializer(ReadOnlyModelSerializer):
    genres = GenreSerializer(many=True)
    collaborators = ArtistReadOnlySerializer(many=True)

    class Meta:
        model = Track
        exclude = ('file', 'album')
