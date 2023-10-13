from rest_framework import serializers
from src.music.models import Single
from src.music.serializers import TrackSerializer


class SingleSerializer(serializers.ModelSerializer):
    track = 'TrackSerializer'

    class Meta:
        model = Single
        fields = '__all__'
