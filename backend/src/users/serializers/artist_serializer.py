from rest_framework import serializers

from src.users.models import Artist
from src.users.serializers import UserSerializer


class ArtistSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Artist
        fields = (
            'user',
            'stage_name',
            'firstname',
            'lastname',
            'patronymic',
        )

    def create(self, validated_data):
        user = UserSerializer(data=validated_data.pop('user'))
        user.is_valid(raise_exception=True)
        user_instance = user.save()
        listener = Artist.objects.create(user=user_instance, **validated_data)
        return listener
