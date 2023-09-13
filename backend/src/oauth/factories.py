import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'password', 'email', 'date_of_birth')

    username = factory.Faker('name')
    password = factory.django.Password('pw')
    email = factory.Faker('email')
    date_of_birth = factory.Faker('date_of_birth')
