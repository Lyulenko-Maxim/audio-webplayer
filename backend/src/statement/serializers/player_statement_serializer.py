from rest_framework import serializers

from shared.serializers import ReadOnlyModelSerializer
from src.statement.models.player_statement import PlayerStatement
from src.statement.serializers import ContextSerializer


class PlayerStatementSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    context = ContextSerializer(required=False)

    class Meta:
        model = PlayerStatement
        fields = '__all__'


class IsPlayingStateSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = PlayerStatement
        fields = ('is_playing',)


class VolumeStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStatement
        fields = ('volume',)


class CurrentPositionStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStatement
        fields = ('current_position',)


class ShuffleStateSerializer(ReadOnlyModelSerializer):
    class Meta:
        model = PlayerStatement
        fields = ('is_shuffle',)


class RepeatStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerStatement
        fields = ('repeat_state',)


class ContextStateSerializer(serializers.ModelSerializer):
    context = ContextSerializer(required=False, allow_null=True)

    class Meta:
        model = PlayerStatement
        fields = ('context',)
