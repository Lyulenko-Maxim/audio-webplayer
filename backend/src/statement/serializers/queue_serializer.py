from rest_framework import serializers

from src.statement.models import Queue
from src.tracks.serializers import TrackReadOnlySerializer


class QueueSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    tracks = TrackReadOnlySerializer(many=True)

    class Meta:
        model = Queue
        fields = '__all__'
