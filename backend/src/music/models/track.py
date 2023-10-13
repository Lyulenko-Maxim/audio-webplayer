from django.db import models

from src.music.models import Album
from src.users.models import Artist


class Track(models.Model):
    """Модель музыкального трека."""

    title = models.CharField(max_length=128, verbose_name='название')
    album = models.ForeignKey(to=Album, on_delete=models.CASCADE, related_name='tracks', verbose_name='альбом', )
    collaborators = models.ManyToManyField(to=Artist, through='Collaboration', verbose_name='коллаборация')
    duration = models.PositiveIntegerField(editable=False, verbose_name='длительность')
    plays = models.PositiveIntegerField(editable=False, verbose_name='прослушивания')

    position = models.PositiveIntegerField(verbose_name='порядковый номер')

    class Meta:
        verbose_name = 'трек'
        verbose_name_plural = 'треки'

    def __str__(self):
        return f'{self.album.artist.stage_name} {self.title}'
