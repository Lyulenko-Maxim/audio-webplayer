from rest_framework import serializers

from src.tracks.models import Collaboration
from src.artists.serializers import ArtistSerializer


class CollaborationReadOnlySerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(read_only=True)

    class Meta:
        model = Collaboration
        fields = '__all__'
