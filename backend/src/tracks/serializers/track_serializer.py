from rest_framework import serializers

from src.artists.serializers import ArtistReadOnlySerializer
from src.genres.serializers.genre_serializer import GenreSerializer
from src.tracks.models import Track


class TrackSerializer(serializers.ModelSerializer):
    collaborators = ArtistReadOnlySerializer(read_only=True, many=True)

    class Meta:
        model = Track
        fields = (
            'id', 'title', 'album', 'file', 'position',
            'duration', 'plays', 'genres', 'collaborators'
        )
        extra_kwargs = {
            'file': {'write_only': True},
            'plays': {'read_only': True},
            'duration': {'read_only': True, 'required': False, },
            'genres': {'required': False},
        }
