from django.contrib.auth import get_user_model
from django.db import models

from src.users.models import Artist, Listener


class Follower(models.Model):
    """Модель подписки"""

    listener = models.ForeignKey(
        to = Listener,
        on_delete = models.CASCADE,
        related_name = 'following',
        verbose_name = 'Подписчик'
    )
    artist = models.ForeignKey(
        to = Artist,
        on_delete = models.CASCADE,
        related_name = 'followers',
        verbose_name = 'Исполнитель'
    )
    followed_at = models.DateTimeField(auto_now_add = True, verbose_name = 'Дата подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ('listener', 'artist')

    def __str__(self):
        return f"{self.listener} подписался на {self.artist.stage_name}"
