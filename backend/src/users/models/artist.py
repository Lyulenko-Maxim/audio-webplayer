from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Artist(models.Model):
    """Модель исполнителя."""

    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name='artist',
        verbose_name='пользователь'
    )
    stage_name = models.CharField(max_length=64, verbose_name='сценическое имя')
    firstname = models.CharField(max_length=64, blank=True, null=True, verbose_name='имя')
    lastname = models.CharField(max_length=64, blank=True, null=True, verbose_name='фамилия')
    patronymic = models.CharField(max_length=64, blank=True, null=True, verbose_name='отчество')

    class Meta:
        verbose_name = 'исполнитель'
        verbose_name_plural = 'исполнители'

    def __str__(self):
        return self.stage_name
