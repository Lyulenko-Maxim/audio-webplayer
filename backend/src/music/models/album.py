from django.db import models
from django.utils import timezone

from src.users.models import Artist


class Album(models.Model):
    """Модель музыкального альбома."""
    title = models.CharField(max_length = 64, verbose_name = 'Название')
    artist = models.ForeignKey(
        to = Artist,
        on_delete = models.CASCADE,
        related_name = 'albums',
        verbose_name = 'Исполнитель',
    )
    duration = models.PositiveIntegerField(editable = False, verbose_name = 'Длительность')
    release = models.DateTimeField(default = timezone.now, verbose_name = 'Дата релиза')

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'

    def __str__(self):
        return f'{self.artist.stage_name} {self.title}'
