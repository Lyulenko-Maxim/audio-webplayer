from django.db import models
from django.utils import timezone

from src.users.models import Artist


class Album(models.Model):
    """Модель музыкального альбома."""
    ALBUM_TYPE_CHOICES = [
        ('album', 'Альбом'),
        ('single', 'Сингл'),
        ('compilation', 'Сборник'),
    ]
    type = models.CharField(choices=ALBUM_TYPE_CHOICES, verbose_name='тип')
    title = models.CharField(max_length=64, verbose_name='название')
    artist = models.ForeignKey(
        to=Artist,
        on_delete=models.CASCADE,
        related_name='albums',
        verbose_name='Исполнитель',
    )
    release = models.DateTimeField(default=timezone.now, verbose_name='дата релиза')

    class Meta:
        verbose_name = 'альбом'
        verbose_name_plural = 'альбомы'

    def __str__(self):
        return f'{self.artist.stage_name} {self.title}'
