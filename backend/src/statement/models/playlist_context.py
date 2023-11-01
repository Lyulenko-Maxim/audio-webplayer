from django.db import models

from src.playlists.models import Playlist
from src.statement.models import Context


class PlaylistContext(Context):
    playlist = models.ForeignKey(
        to=Playlist,
        on_delete=models.CASCADE,
        related_name='context',
        verbose_name="плейлист"
    )

    class Meta:
        db_table = 'statement_playlist_context'
        verbose_name = 'контекст плейлиста'
        verbose_name_plural = 'контексты плейлистов'
