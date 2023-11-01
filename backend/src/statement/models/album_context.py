from django.db import models

from src.albums.models import Album
from src.statement.models import Context


class AlbumContext(Context):
    album = models.ForeignKey(
        to=Album,
        on_delete=models.CASCADE,
        related_name='context',
        verbose_name="альбом"
    )

    class Meta:
        db_table = 'statement_album_context'
        verbose_name = 'контекст альбома'
        verbose_name_plural = 'контексты альбомов'
