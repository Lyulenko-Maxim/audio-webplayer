from django.db import models

from src.users.models import User


class Listener(models.Model):
    """Модель слушателя"""

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='listener',
        verbose_name='пользователь'
    )

    class Meta:
        verbose_name = 'слушатель'
        verbose_name_plural = 'слушатели'

    def __str__(self):
        return self.user.username
