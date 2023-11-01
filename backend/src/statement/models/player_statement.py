from django.contrib.auth import get_user_model
from django.db import models

from src.statement.models import Context

User = get_user_model()


class PlayerStatement(models.Model):
    REPEAT_CHOICES = [
        ('off', 'выключено'),
        ('track', 'повторить текущий трек'),
        ('context', 'повторить контекст'),
    ]
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='player_statement',
        verbose_name='пользователь'
    )
    is_playing = models.BooleanField(default=False, verbose_name='воспроизводится')
    volume = models.FloatField(default=0.5, verbose_name='громкость')
    current_position = models.PositiveIntegerField(default=0, verbose_name='текущая позиция в секундах')
    is_shuffle = models.BooleanField(default=False, verbose_name='перемешивается')
    repeat_state = models.CharField(
        max_length=10,
        choices=REPEAT_CHOICES,
        default='off',
        verbose_name='состояние повтора'
    )
    context = models.OneToOneField(
        to=Context,
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='player_statement',
        verbose_name='контекст'
    )

    class Meta:
        db_table = 'statement_player_statement'
        verbose_name = 'статус плеера'
        verbose_name_plural = 'статусы плееров'
