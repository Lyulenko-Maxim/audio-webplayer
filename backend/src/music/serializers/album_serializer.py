from rest_framework import serializers

from src.music.models import Album


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
        extra_kwargs = {'artist': {'read_only': True}}
