from rest_framework import serializers
from src.playlists.models.playlist import Playlist


class PlaylistSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Playlist
        # fields = '__all__'
        exclude = ('tracks',)
        extra_kwargs = {'created': {'read_only': True, }, }
