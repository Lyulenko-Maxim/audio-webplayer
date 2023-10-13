from rest_framework import generics, status
from rest_framework.response import Response

from src.oauth.permissions import IsAnonymous
from src.users.serializers import ArtistSerializer


class ArtistSignUpView(generics.GenericAPIView):
    serializer_class = ArtistSerializer
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
