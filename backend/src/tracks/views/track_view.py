from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shared.helpers import shift_positions
from src.tracks.helpers import set_track_serializer_duration
from src.tracks.models import Track
from src.tracks.serializers import CollaborationSerializer, TrackSerializer
from src.users.permissions import IsArtist


class TrackView(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = TrackSerializer
    queryset = (
        Track.objects
        .prefetch_related('genres')
        .prefetch_related('collaborators')
        .select_related('album')
    )

    def list(self, request):
        artist = request.user.artist
        tracks = self.get_queryset().filter(album__artist=artist)
        serializer = self.get_serializer(tracks, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer = set_track_serializer_duration(serializer=serializer)
        serializer.save()

    def perform_update(self, serializer):
        set_track_serializer_duration(serializer=serializer)
        shift_positions(instance=serializer.instance, new_position=serializer.validated_data['position'])
        serializer.save()

    def perform_destroy(self, instance):
        shift_positions(instance=instance)
        instance.delete()

    @action(detail=False, methods=['post'], url_path='add-collaborator', serializer_class=CollaborationSerializer)
    def add_collaborator(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'message': 'Добавлен коллаборатор.'}, status=status.HTTP_201_CREATED)
