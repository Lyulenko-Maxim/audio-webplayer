from django.contrib.auth import get_user_model
from rest_framework import serializers

from src.users.models import UserProfile

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('id', 'user')
