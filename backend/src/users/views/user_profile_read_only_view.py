from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ReadOnlyModelViewSet

from src.users.models import UserProfile
from src.users.serializers import UserProfileReadOnlySerializer

User = get_user_model()


class UserProfileReadOnlyView(ReadOnlyModelViewSet):
    queryset = UserProfile.objects
    serializer_class = UserProfileReadOnlySerializer
    permission_classes = [AllowAny]
