from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone
from src.tracks.models import Track

User = get_user_model()


def playlist_cover_upload_to(instance, filename):
    extension = filename.split('.')[-1]
    return f'users/{instance.user.id}/playlists/{instance.id}/cover.{extension}'


class Playlist(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='playlists',
        verbose_name='пользователь'
    )
    title = models.CharField(max_length=64, verbose_name='название', )
    tracks = models.ManyToManyField(to=Track, through='PlaylistTrack', verbose_name='треки')
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    cover = models.ImageField(
        default='artists/default/albums/default/cover.png',
        blank=True,
        upload_to=playlist_cover_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg']), ],
        verbose_name='обложка',
    )
    created = models.DateTimeField(default=timezone.now, verbose_name='создан')
    is_public = models.BooleanField(default=False, verbose_name='публичный')

    class Meta:
        verbose_name = 'плейлист'
        verbose_name_plural = 'плейлисты'

    def __str__(self):
        return self.title
