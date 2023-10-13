from django.db import models

from src.users.models import Artist, Listener


class Follow(models.Model):
    """Модель подписки"""

    listener = models.ForeignKey(
        to=Listener,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='подписчик'
    )
    artist = models.ForeignKey(
        to=Artist,
        on_delete=models.CASCADE,
        related_name='followers',
        verbose_name='исполнитель'
    )
    followed_at = models.DateTimeField(auto_now_add=True, verbose_name='дата подписки')

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        unique_together = ('listener', 'artist')

    def __str__(self):
        return f"{self.listener.user.username} подписан на {self.artist.stage_name}"
