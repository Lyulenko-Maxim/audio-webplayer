from django.apps import apps
from django.db import models
from django.db.models import Prefetch


class AlbumQuerySet(models.QuerySet):
    def with_tracks(self):
        """
        Prefetch the Track objects associated with this Album.
        """
        track = apps.get_model(app_label='music', model_name='Track')
        return self.prefetch_related(Prefetch(lookup='tracks', queryset=track.objects.all()))
