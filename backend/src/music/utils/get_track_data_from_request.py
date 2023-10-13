from rest_framework import serializers, status
from rest_framework.request import Request
from rest_framework.serializers import Serializer


def get_track_data_from_request(request: Request, serializer: Serializer) -> dict:
    """Получает данные трека из запроса."""

    serializer.is_valid(raise_exception = True)
    track_data = serializer.validated_data.get('track')
    artist = request.user.artist
    track_data['artist'] = artist
    return track_data
