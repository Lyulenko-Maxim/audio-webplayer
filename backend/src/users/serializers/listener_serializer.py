from rest_framework import serializers

from src.users.models import Listener
from src.users.serializers import UserSerializer


class ListenerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Listener
        fields = ('user',)

    def create(self, validated_data):
        user = UserSerializer(data = validated_data.pop('user'))
        user.is_valid(raise_exception = True)
        user_instance = user.save()
        listener = Listener.objects.create(user = user_instance, **validated_data)
        return listener
