from src.playlists.models.playlist import Playlist
from src.tracks.serializers import TrackReadOnlySerializer
from src.users.serializers import UserProfileReadOnlySerializer
from shared.serializers import ReadOnlyModelSerializer


class PlaylistWithTracksReadOnlySerializer(ReadOnlyModelSerializer):
    tracks = TrackReadOnlySerializer(many=True)
    user = UserProfileReadOnlySerializer()

    class Meta:
        model = Playlist
        fields = '__all__'
