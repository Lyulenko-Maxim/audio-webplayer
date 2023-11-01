from rest_framework import serializers

from shared.serializers import ReadOnlyModelSerializer
from src.statement.models import Context
from src.tracks.serializers import TrackReadOnlySerializer


class ContextSerializer(serializers.ModelSerializer):
    class Meta:
        model = Context
        fields = '__all__'


class ContextReadOnlySerializer(ReadOnlyModelSerializer):
    current_track = TrackReadOnlySerializer()

    class Meta:
        model = Context
        fields = ('id', 'type', 'context_id', 'current_track')

    def validate(self, attrs):
        context_type = attrs.get('type')
        context_id = attrs.get('context_id')

        if context_id != context_type:
            raise serializers.ValidationError('type и id должны быть указаны вместе или же не указаны вовсе')

        return attrs
