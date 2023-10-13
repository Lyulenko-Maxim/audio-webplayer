from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.oauth.authentication import JWTAuthentication
from src.music.serializers import AlbumSerializer


class CreateAlbumView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = AlbumSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        artist = request.user.artist
        serializer.save(artist = artist)
        return Response(serializer.validated_data, status = status.HTTP_201_CREATED)
