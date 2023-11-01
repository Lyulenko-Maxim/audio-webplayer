from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models

User = get_user_model()


def artist_photo_upload_to(instance, filename: str) -> str:
    extension = filename.split('.')[-1]
    return f'artists/{instance.id}/photo.{extension}'


def artist_header_upload_to(instance, filename: str) -> str:
    extension = filename.split('.')[-1]
    return f'artists/{instance.id}/header.{extension}'


class Artist(models.Model):
    """Модель исполнителя."""

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='artist',
        verbose_name='пользователь'
    )
    stage_name = models.CharField(max_length=64, blank=True, null=True, verbose_name='сценическое имя')
    firstname = models.CharField(max_length=64, blank=True, null=True, verbose_name='имя')
    lastname = models.CharField(max_length=64, blank=True, null=True, verbose_name='фамилия')
    patronymic = models.CharField(max_length=64, blank=True, null=True, verbose_name='отчество')
    bio = models.TextField(blank=True, null=True, verbose_name='биография')
    photo = models.ImageField(
        default='artists/default/photo.png',
        blank=True,
        upload_to=artist_photo_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']), ],
        verbose_name='фото',
    )
    header = models.ImageField(
        default='/artists/default/header.png',
        blank=True,
        upload_to=artist_header_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']), ],
        verbose_name='шапка',
    )
    is_verified = models.BooleanField(default=False, verbose_name='верифицирован')

    class Meta:
        verbose_name = 'исполнитель'
        verbose_name_plural = 'исполнители'

    def __str__(self):
        return self.stage_name

    def save(self, *args, **kwargs):
        self.set_default_name()
        super(Artist, self).save(*args, **kwargs)

    def set_default_name(self):
        if not self.stage_name:
            self.stage_name = self.user.username
