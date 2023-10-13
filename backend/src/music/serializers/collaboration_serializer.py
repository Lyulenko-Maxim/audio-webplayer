from rest_framework import serializers

from src.music.models import Collaboration


class CollaborationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collaboration
        fields = '__all__'
