from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone

from src.users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Модель пользователя"""

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
    email = models.EmailField(unique = True, blank = False, null = False, verbose_name = 'Электронная почта')
    gender = models.CharField(max_length = 1, choices = GENDER_CHOICES, default = 'N', verbose_name = 'Гендер')
    date_of_birth = models.DateField(blank = False, null = False, verbose_name = 'Дата рождения')
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


class Listener(models.Model):
    """Модель слушателя"""

    user = models.OneToOneField(
        to = User,
        on_delete = models.CASCADE,
        related_name = 'listener',
        verbose_name = 'Пользователь'
    )

    class Meta:
        verbose_name = 'Слушатель'
        verbose_name_plural = 'Слушатели'

    def __str__(self):
        return self.user.username


class Artist(models.Model):
    """Модель исполнителя"""

    user = models.OneToOneField(
        to = User,
        on_delete = models.CASCADE,
        related_name = 'user',
        verbose_name = 'Пользователь'
    )
    stage_name = models.CharField(max_length = 64, blank = False, null = False, verbose_name = 'Сценическое имя')
    firstname = models.CharField(max_length = 64, blank = True, null = True, verbose_name = 'Имя')
    lastname = models.CharField(max_length = 64, blank = True, null = True, verbose_name = 'Фамилия')
    patronymic = models.CharField(max_length = 64, blank = True, null = True, verbose_name = 'Отчество')

    tracks_count = models.PositiveIntegerField(default = 0, verbose_name = 'Количество треков')
    albums_count = models.PositiveIntegerField(default = 0, verbose_name = 'Количество альбомов')
    followers_count = models.PositiveIntegerField(default = 0, verbose_name = 'Количество подписчиков')
    listens_count = models.PositiveIntegerField(default = 0, verbose_name = 'Количество прослушиваний')

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    def __str__(self):
        return self.stage_name


class Follower(models.Model):
    """Модель подписки"""

    listener = models.ForeignKey(
        to = User,
        on_delete = models.CASCADE,
        related_name = 'following',
        verbose_name = 'Подписчик'
    )
    artist = models.ForeignKey(
        to = Artist,
        on_delete = models.CASCADE,
        related_name = 'followers',
        verbose_name = 'Исполнитель'
    )
    followed_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('listener', 'artist')

    def __str__(self):
        return f"{self.listener} подписался на {self.artist.stage_name}"
