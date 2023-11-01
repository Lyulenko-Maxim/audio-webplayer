from rest_framework import serializers
from src.playlists.models.playlist_track import PlaylistTrack


class PlaylistTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistTrack
        fields = ('id', 'track', 'position')
