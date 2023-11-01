from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django_countries.fields import CountryField


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""

    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        ('O', 'Другое'),
        ('N', 'Не хочу отвечать'),
    )

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=32,
        unique=True,
        validators=[username_validator],
        verbose_name='имя пользователя'
    )
    password = models.CharField(max_length=128, verbose_name='пароль')
    email = models.EmailField(unique=True, verbose_name='электронная почта')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N', verbose_name='гендер')
    date_of_birth = models.DateField(verbose_name='дата рождения')
    country = CountryField(verbose_name='страна')
    receive_promotions = models.BooleanField(default=False, verbose_name='получать рекламу')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='дата регистрации')
    is_staff = models.BooleanField(default=False, verbose_name='администратор')
    is_artist = models.BooleanField(default=False, verbose_name='исполнитель')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.username

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
