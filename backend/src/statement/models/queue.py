from django.contrib.auth import get_user_model
from django.db import models

from src.tracks.models import Track

User = get_user_model()


class Queue(models.Model):
    """Модель очереди."""
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='queue',
        verbose_name='очередь'
    )
    tracks = models.ManyToManyField(to=Track, through='QueueTrack', verbose_name='треки')

    class Meta:
        verbose_name = 'очередь'
        verbose_name_plural = 'очереди'
