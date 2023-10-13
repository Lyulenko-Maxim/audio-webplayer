from rest_framework import serializers
from src.music.models import Track


class TrackInAlbumSerializer(serializers.ModelSerializer):
    track = 'TrackSerializer'
    album = 'AlbumSerializer'

    class Meta:
        model = Track
        fields = '__all__'
