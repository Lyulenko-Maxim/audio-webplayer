from src.playlists.models.playlist_track import PlaylistTrack
from src.tracks.serializers import TrackReadOnlySerializer
from shared.serializers import ReadOnlyModelSerializer


class PlaylistTrackReadOnlySerializer(ReadOnlyModelSerializer):
    track = TrackReadOnlySerializer()

    class Meta:
        model = PlaylistTrack
        fields = '__all__'
