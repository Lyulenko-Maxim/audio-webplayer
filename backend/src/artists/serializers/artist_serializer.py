from rest_framework import serializers

from src.users.models import Artist


class ArtistSerializer(serializers.ModelSerializer):
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
        extra_kwargs = {'is_verified': {'read_only': True}}
