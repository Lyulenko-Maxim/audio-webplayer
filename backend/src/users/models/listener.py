from django.db import models

from src.users.models import User


class Listener(models.Model):
    """Модель слушателя"""

    user = models.OneToOneField(
        to = User,
        on_delete = models.CASCADE,
        verbose_name = 'Пользователь'
    )

    class Meta:
        verbose_name = 'Слушатель'
        verbose_name_plural = 'Слушатели'

    def __str__(self):
        return self.user.username
