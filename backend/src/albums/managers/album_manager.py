from django.db import models

from src.albums.querysets.album_queryset import AlbumQuerySet


class AlbumManager(models.Manager):
    def get_queryset(self):
        return AlbumQuerySet(model=self.model, using=self._db)

    def with_tracks(self):
        return self.get_queryset().with_tracks()
