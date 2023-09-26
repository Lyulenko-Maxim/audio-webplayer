from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Artist(models.Model):
    """Модель исполнителя."""

    user = models.OneToOneField(
        to = User,
        on_delete = models.CASCADE,
        related_name = 'user',
        verbose_name = 'Пользователь'
    )
    stage_name = models.CharField(max_length = 64, verbose_name = 'Сценическое имя')
    firstname = models.CharField(max_length = 64, blank = True, null = True, verbose_name = 'Имя')
    lastname = models.CharField(max_length = 64, blank = True, null = True, verbose_name = 'Фамилия')
    patronymic = models.CharField(max_length = 64, blank = True, null = True, verbose_name = 'Отчество')

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'

    def __str__(self):
        return self.stage_name
