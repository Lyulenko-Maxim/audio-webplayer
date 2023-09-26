from django.db import models
from django.utils import timezone

from src.users.models import Artist


class Track(models.Model):
    """Модель музыкального трека."""

    title = models.CharField(max_length = 64, verbose_name = 'Название')
    artist = models.ForeignKey(
        to = Artist,
        on_delete = models.CASCADE,
        related_name = 'tracks',
        verbose_name = 'Исполнитель',
    )
    collaborators = models.ManyToManyField(to = Artist, through = 'Collaboration', verbose_name = 'Коллаборация')
    release = models.DateField(default = timezone.now, verbose_name = 'Дата релиза')
    duration = models.PositiveIntegerField(editable = False, verbose_name = 'Длительность')
    plays = models.PositiveIntegerField(editable = False, verbose_name = 'Прослушивания')

    class Meta:
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'

    def __str__(self):
        return f'{self.artist.stage_name} {self.title}'
