from django.db.models import Prefetch
from rest_framework import permissions, viewsets

from src.genres.models import Genre
from src.tracks.models import Collaboration
from src.tracks.models import Track
from src.tracks.serializers import TrackReadOnlySerializer


class TrackReadOnlyView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = TrackReadOnlySerializer
    queryset = (
        Track.objects
        .prefetch_related(
            Prefetch(lookup='genres', queryset=Genre.objects.all()),
            Prefetch(lookup='collaborators', queryset=Collaboration.objects.order_by('position'))
        )
        .select_related('album')
    )
