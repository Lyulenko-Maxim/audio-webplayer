from rest_framework import serializers

# from src.music.serializers import CollaborationSerializer
from src.music.models import Track


class TrackSerializer(serializers.ModelSerializer):
    collaborators = 'CollaborationSerializer'

    class Meta:
        model = Track
        fields = '__all__'
