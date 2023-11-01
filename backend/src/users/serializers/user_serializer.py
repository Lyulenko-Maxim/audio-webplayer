from django.contrib.auth import get_user_model
from django_countries.serializers import CountryFieldMixin
from rest_framework import serializers

from src.users.serializers import UserProfileSerializer

User = get_user_model()


class UserSerializer(CountryFieldMixin, serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'gender',
            'date_of_birth',
            'country',
            'receive_promotions',
            'profile',
            'is_artist',
        )
        extra_kwargs = {
            'username': {'read_only': True},
            'is_artist': {'read_only': True},

            'email': {'required': False},
            'gender': {'required': False},
            'date_of_birth': {'required': False},
            'country': {'required': False},
            'receive_promotions': {'required': False},
        }
