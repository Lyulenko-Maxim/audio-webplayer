from django.db import models

from src.tracks.models import Track
from src.playlists.models.playlist import Playlist


class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(to=Playlist, on_delete=models.CASCADE, verbose_name='плейлист')
    track = models.ForeignKey(to=Track, on_delete=models.CASCADE, verbose_name='трек')
    position = models.PositiveIntegerField(verbose_name='порядковый номер')

    class Meta:
        db_table = 'playlists_playlist_track'
        unique_together = ('playlist', 'track')
        verbose_name = 'трек в плейлисте'
        verbose_name_plural = 'треки в плейлисте'

    def __str__(self):
        return f'{self.playlist.title} {self.track.title}'
