from django.db import models

from src.tracks.models import Track
from src.users.models import Artist


class Collaboration(models.Model):
    """Модель коллаборации."""

    track = models.ForeignKey(to=Track, on_delete=models.CASCADE, verbose_name='трек')
    artist = models.ForeignKey(to=Artist, on_delete=models.CASCADE, verbose_name='исполнитель')
    position = models.PositiveIntegerField(verbose_name='порядковый номер')

    class Meta:
        unique_together = ('track', 'artist')
        verbose_name = 'коллаборация'
        verbose_name_plural = 'коллаборации'

    def __str__(self):
        return f'{self.artist.stage_name} {self.track.title}'
