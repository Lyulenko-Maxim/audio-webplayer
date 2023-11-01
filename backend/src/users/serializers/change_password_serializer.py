from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        max_length=128,
        write_only=True,
        label='старый пароль',
    )
    new_password = serializers.CharField(
        required=True,
        max_length=128,
        write_only=True,
        label='новый пароль',
    )
    new_password_confirmation = serializers.CharField(
        required=True,
        max_length=128,
        write_only=True,
        label='повторите пароль',
    )

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_confirmation = attrs.get('new_password_confirmation')

        if not self.context['request'].user.check_password(old_password):
            raise serializers.ValidationError('Старый пароль введен неверно.')

        if new_password != new_password_confirmation:
            raise serializers.ValidationError('Пароли не совпадают.')

        if new_password == old_password:
            raise serializers.ValidationError('Новый пароль не может совпадать со старым.')

        return attrs


