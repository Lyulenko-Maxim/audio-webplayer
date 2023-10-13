from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from src.music.serializers import SingleSerializer
from src.users.permissions import IsArtist

from src.music.utils import (
    create_track,
    create_collaborations,
    get_track_data_from_request
)


class CreateSingleView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = SingleSerializer

    def perform_create(self, serializer):
        """Перед созданием сингла создает модели трека и коллабораций."""

        track_data = get_track_data_from_request(request=self.request, serializer=serializer)
        collaborators = track_data.get('collaborators', [])

        track = create_track(track_data=track_data)
        create_collaborations(track=track, artists=collaborators)

        serializer.save(track=track, artist=track.artist)
