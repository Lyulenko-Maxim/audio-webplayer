from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response

from src.oauth.permissions import IsAnonymous
from src.users.serializers.listener_serializer import ListenerSerializer

User = get_user_model()


class ListenerSignUpView(generics.GenericAPIView):
    serializer_class = ListenerSerializer
    permission_classes = [IsAnonymous]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
