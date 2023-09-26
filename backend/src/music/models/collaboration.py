from django.db import models

from src.users.models import Artist
from src.music.models import Track


class Collaboration(models.Model):
    """Модель коллаборации."""

    track = models.OneToOneField(to = Track, on_delete = models.CASCADE, verbose_name = 'Трек')
    artist = models.ForeignKey(to = Artist, on_delete = models.CASCADE, verbose_name = 'Исполнители')

    class Meta:
        verbose_name = 'Коллаборация'
        verbose_name_plural = 'Коллаборации'

    def __str__(self):
        return f'{self.track.artist.stage_name} {self.track.title}'
