from rest_framework import serializers

from src.tracks.models import Collaboration


class CollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaboration
        fields = ('id', 'artist', 'track')

    def validate_artist(self, value):
        if value == self.context['request'].user.artist:
            raise serializers.ValidationError("Вы не можете добавить сами себя в коллаборацию.")
        return value
