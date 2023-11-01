from django.db import models


class Genre(models.Model):
    """Модель музыкального жанра."""

    name = models.CharField(max_length=64, verbose_name='жанр')

    class Meta:
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name
