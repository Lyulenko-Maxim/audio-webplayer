from django.contrib.auth import get_user_model
from rest_framework import serializers

from shared.serializers import ReadOnlyModelSerializer
from src.users.models import UserProfile

User = get_user_model()


class UserProfileReadOnlySerializer(ReadOnlyModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'name', 'photo')
