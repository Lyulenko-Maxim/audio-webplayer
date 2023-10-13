from rest_framework import generics, serializers, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from src.music.models import Album
from src.music.utils import (
    create_collaborations,
    create_track,
    get_track_data_from_request
)
from src.music.serializers import TrackInAlbumSerializer
from src.users.permissions import IsArtist


class AddTrackToAlbumView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = TrackInAlbumSerializer

    def perform_create(self, serializer):
        album_data = serializer.validated_data.get('album')

        if not album_data:
            raise serializers.ValidationError(
                detail = 'Данные о треке отсутствуют.',
                code = status.HTTP_400_BAD_REQUEST
            )

        album = get_object_or_404(Album, id = album_data.get('id'))

        track_data = get_track_data_from_request(request = self.request, serializer = serializer)
        collaborators = track_data.get('collaborators', [])
        track = create_track(track_data = track_data)
        create_collaborations(track = track, artists = collaborators)

        serializer.save(track = track, album = album)
