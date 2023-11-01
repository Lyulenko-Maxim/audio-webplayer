from rest_framework import serializers

from shared.serializers import ReadOnlyModelSerializer
from src.users.models import Artist


class ArtistReadOnlySerializer(ReadOnlyModelSerializer):
    class Meta:
        model = Artist
        fields = (
            'id',
            'stage_name',
            'firstname',
            'lastname',
            'patronymic',
            'bio',
            'photo',
            'header',
            'is_verified',
        )
