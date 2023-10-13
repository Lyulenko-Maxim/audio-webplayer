from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password_repeated = serializers.CharField(
        max_length = 128,
        write_only = True,
        label = 'Повторите пароль'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'password_repeated',
            'email',
            'gender',
            'date_of_birth',
            'receive_promotions',
        )
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        try:
            if data['password'] != data['password_repeated']:
                raise serializers.ValidationError('Пароли не совпадают.')
        except KeyError as e:
            raise serializers.ValidationError(e)
        return data

    def create(self, validated_data):
        validated_data.pop('password_repeated')
        return User.objects.create_user(
            username = validated_data.pop('username'),
            email = validated_data.pop('email'),
            password = validated_data.pop('password'),
            **validated_data,
        )
