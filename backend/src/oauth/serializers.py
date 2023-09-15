from django.contrib.auth import get_user_model
from rest_framework import serializers

from src.users.models import Artist, Listener

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'role', 'username', 'email', 'password', 'date_of_birth']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(raw_password = password)
            instance.save()
        return instance


class ListenerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listener
        fields = ['user']


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['user', 'stage_name', 'firstname', 'lastname', 'patronymic']
