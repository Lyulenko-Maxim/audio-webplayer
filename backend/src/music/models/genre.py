from django.db import models


class Genre(models.Model):
    """Модель музыкального жанра."""

    name = models.CharField(max_length = 32, verbose_name = 'Жанр')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name
