from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from src.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя."""

    objects = UserManager()

    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        ('O', 'Другое'),
        ('N', 'Не хочу отвечать'),
    )

    ROLE_CHOICES = (
        ('listener', 'Слушатель'),
        ('artist', 'Исполнитель'),
    )

    role = models.CharField(max_length = 10, choices = ROLE_CHOICES, default = 'listener', verbose_name = 'Роль')
    username = models.CharField(max_length = 32, unique = True, verbose_name = 'Имя пользователя')
    password = models.CharField(max_length = 128, verbose_name = 'Пароль')
    email = models.EmailField(unique = True, verbose_name = 'Электронная почта')
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, default = 'N', verbose_name = 'Гендер')
    date_of_birth = models.DateField(verbose_name = 'Дата рождения')
    receive_promotions = models.BooleanField(default = False, verbose_name = 'Получать рекламу')
    date_joined = models.DateTimeField(default = timezone.now, verbose_name = 'Дата регистрации')
    is_staff = models.BooleanField(default = False, verbose_name = 'Администратор')

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email = None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)
