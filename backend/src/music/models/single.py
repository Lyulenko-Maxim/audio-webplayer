from django.db import models
from django.utils import timezone

from src.music.models import Track
from src.users.models import Artist


class Single(models.Model):
    """Модель музыкального сингла."""
    track = models.OneToOneField(to = Track, on_delete = models.CASCADE, verbose_name = 'Трек')
    artist = models.ForeignKey(to = Artist, on_delete = models.CASCADE, verbose_name = 'Исполнитель')

    release = models.DateTimeField(default = timezone.now, verbose_name = 'Дата релиза')

    class Meta:
        verbose_name = 'Сингл'
        verbose_name_plural = 'Синглы'

    def __str__(self):
        return f'{self.track.artist.stage_name} {self.track.title}'
