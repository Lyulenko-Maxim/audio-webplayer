from rest_framework.generics import CreateAPIView

from src.authentication.permissions import IsAnonymous
from src.authentication.serializers import SignUpSerializer


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = [IsAnonymous]
