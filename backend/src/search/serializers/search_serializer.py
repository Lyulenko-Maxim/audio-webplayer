from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    q = serializers.CharField(max_length=255, required=False)
    albums = serializers.BooleanField(default=False, required=False)
    tracks = serializers.BooleanField(default=False, required=False)
    artists = serializers.BooleanField(default=False, required=False)
