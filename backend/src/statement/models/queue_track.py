from django.db import models

from src.statement.models import Queue
from src.tracks.models import Track


class QueueTrack(models.Model):
    track = models.ForeignKey(to=Track, on_delete=models.CASCADE)
    queue = models.ForeignKey(to=Queue, on_delete=models.CASCADE)

    class Meta:
        db_table = 'statement_queue_track'
        unique_together = ('track', 'queue')
