from django.db import models
from polymorphic.models import PolymorphicModel

from src.tracks.models import Track


class Context(PolymorphicModel):
    CONTEXT_TYPE_CHOICES = [
        ('album', 'альбом'),
        ('playlist', 'плейлист'),
    ]
    type = models.CharField(choices=CONTEXT_TYPE_CHOICES, null=True, blank=True, verbose_name='тип')
    context_id = models.PositiveIntegerField(null=True, blank=True, verbose_name='контекст')
    current_track = models.ForeignKey(
        to=Track,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='текущий трек'
    )

    class Meta:
        verbose_name = 'контекст'
        verbose_name_plural = 'контексты'
