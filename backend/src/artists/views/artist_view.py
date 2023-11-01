from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.artists.models import Artist
from src.artists.serializers import ArtistSerializer
from src.users.permissions import IsArtist


class ArtistView(GenericViewSet):
    queryset = Artist.objects
    permission_classes = [IsAuthenticated, IsArtist]
    serializer_class = ArtistSerializer

    def list(self, request):
        artist = get_object_or_404(Artist, user=request.user)
        serializer = self.get_serializer(artist)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], url_path='edit', serializer_class=ArtistSerializer)
    def update_artist(self, request):
        artist = get_object_or_404(Artist, user=request.user)
        serializer = self.get_serializer(artist, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data={'message': 'Профиль успешно изменен'})
