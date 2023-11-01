from src.playlists.models.playlist import Playlist
from src.users.serializers import UserProfileReadOnlySerializer
from shared.serializers import ReadOnlyModelSerializer


class PlaylistReadOnlySerializer(ReadOnlyModelSerializer):
    user = UserProfileReadOnlySerializer()

    class Meta:
        model = Playlist
        exclude = ('tracks',)
