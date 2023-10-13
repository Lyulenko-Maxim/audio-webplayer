# from django.db import models
#
# from src.music.models import Track, Album
#
#
# # class TrackInAlbum(models.Model):
# #     """Модель музыкального трека в альбоме."""
# #
# #     track = models.OneToOneField(to=Track, on_delete=models.CASCADE, verbose_name='Трек')
# #     album = models.ForeignKey(to=Album, on_delete=models.CASCADE, verbose_name='Альбом')
# #
# #     class Meta:
# #         db_table = 'music_track_in_album'
# #         verbose_name = 'Трек в альбоме'
# #         verbose_name_plural = 'Треки в альбомах'
# #
# #     def __str__(self):
# #         return f'{self.album.title} {self.track.title}'
