from django.db import models
from django.core.validators import FileExtensionValidator
from src.albums.models import Album
from src.genres.models import Genre
from src.users.models import Artist


def track_file_upload_to(instance, filename: str) -> str:
    extension = filename.split('.')[-1]
    return f'artists/{instance.album.artist.id}/albums/{instance.album.id}/tracks/{instance.title}.{extension}'


class Track(models.Model):
    """Модель музыкального трека."""

    title = models.CharField(max_length=128, verbose_name='название')
    genres = models.ManyToManyField(to=Genre, verbose_name='жанры')
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, related_name='tracks', verbose_name='альбом', )
    collaborators = models.ManyToManyField(to=Artist, through='Collaboration', verbose_name='коллаборация')
    is_explicit = models.BooleanField(default=False, verbose_name='нецензурный контент')
    duration = models.PositiveIntegerField(editable=False, blank=True, null=True, verbose_name='длительность')
    plays = models.PositiveIntegerField(editable=False, default=0, verbose_name='прослушивания')
    position = models.PositiveIntegerField(verbose_name='порядковый номер')
    file = models.FileField(
        upload_to=track_file_upload_to,
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])]
    )

    class Meta:
        verbose_name = 'трек'
        verbose_name_plural = 'треки'

    def __str__(self):
        return f'{self.album.artist.stage_name} {self.title}'
