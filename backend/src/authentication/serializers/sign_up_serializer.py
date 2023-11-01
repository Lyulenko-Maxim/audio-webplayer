from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class SignUpSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(
        max_length=128,
        write_only=True,
        label='Повторите пароль'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password_confirmation',
            'email',
            'gender',
            'date_of_birth',
            'country',
            'receive_promotions',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_confirmation'):
            raise serializers.ValidationError('Пароли не совпадают.')

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        _ = validated_data.pop('password_confirmation')
        user = User.objects.create_user(password=password, **validated_data)
        user.set_password(password)
        user.save()
        return user
