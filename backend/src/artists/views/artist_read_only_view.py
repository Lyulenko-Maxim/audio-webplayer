from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from src.artists.models import Artist
from src.artists.serializers import ArtistReadOnlySerializer

User = get_user_model()


class ArtistReadOnlyView(ReadOnlyModelViewSet):
    queryset = Artist.objects
    serializer_class = ArtistReadOnlySerializer
    permission_classes = [AllowAny]
