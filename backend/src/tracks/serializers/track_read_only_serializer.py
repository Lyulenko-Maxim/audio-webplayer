from src.artists.serializers import ArtistReadOnlySerializer
from src.genres.serializers.genre_serializer import GenreSerializer
from src.tracks.models import Track
from src.albums.serializers import AlbumReadOnlySerializer
from shared.serializers import ReadOnlyModelSerializer
from src.tracks.serializers import CollaborationReadOnlySerializer


class TrackReadOnlySerializer(ReadOnlyModelSerializer):
    album = AlbumReadOnlySerializer()
    genres = GenreSerializer(many=True)
    collaborators = ArtistReadOnlySerializer(many=True)

    class Meta:
        model = Track
        fields = ('id', 'title', 'position', 'duration', 'plays', 'genres', 'album', 'collaborators')
