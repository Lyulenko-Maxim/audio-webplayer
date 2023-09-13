from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model
    """

    objects = UserManager()

    GENDER_CHOICES = (
        ('M', 'Мужчина'),
        ('F', 'Женщина'),
        ('O', 'Другое'),
        ('N', 'Не хочу отвечать'),
    )

    username = models.CharField(
        max_length = 32,
        unique = True
    )

    email = models.EmailField(
        unique = True
    )

    gender = models.CharField(
        max_length = 1,
        choices = GENDER_CHOICES,
        default = 'N'
    )

    date_of_birth = models.DateField(
        null = False,
        blank = False
    )

    receive_promotions = models.BooleanField(
        default = False
    )

    date_joined = models.DateTimeField(
        default = timezone.now
    )

    is_staff = models.BooleanField(
        default = False,
    )

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = "email"

    # REQUIRED_FIELDS = ['username', 'email']
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
