from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from src.albums.managers import AlbumManager
from src.users.models import Artist


def album_cover_upload_to(instance, filename: str) -> str:
    extension = filename.split('.')[-1]
    return f'artists/{instance.artist.id}/albums/{instance.id}/cover.{extension}'


class Album(models.Model):
    """Модель музыкального альбома."""

    ALBUM_TYPE_CHOICES = [
        ('album', 'альбом'),
        ('single', 'сингл'),
        ('compilation', 'сборник'),
    ]
    type = models.CharField(choices=ALBUM_TYPE_CHOICES, default='album', verbose_name='тип')
    title = models.CharField(max_length=64, verbose_name='название')
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    release = models.DateTimeField(default=timezone.now, verbose_name='дата релиза')
    cover = models.ImageField(
        default='artists/default/albums/default/cover.png',
        blank=True,
        upload_to=album_cover_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']), ],
        verbose_name='обложка',
    )
    artist = models.ForeignKey(
        to=Artist,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name='Исполнитель',
    )

    objects = AlbumManager()

    class Meta:
        verbose_name = 'альбом'
        verbose_name_plural = 'альбомы'

    def __str__(self):
        return f'{self.artist.stage_name} {self.title}'
