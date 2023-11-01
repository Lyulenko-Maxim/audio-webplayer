from django.db import transaction
from django.db.models import Case, F, PositiveIntegerField, Value, When
from src.playlists.models import PlaylistTrack
from src.tracks.models import Track


def shift_positions(instance: Track | PlaylistTrack, new_position: int = None):
    old_position = instance.position

    if new_position == old_position:
        return

    model = None
    filter_kwargs = dict()
    position_kwargs = dict()

    if isinstance(instance, Track):
        filter_kwargs['album'] = instance.album
        model = Track

    elif isinstance(instance, PlaylistTrack):
        filter_kwargs['playlist'] = instance.playlist
        model = PlaylistTrack

    if new_position:
        increment = 1 if new_position < old_position else -1
        filter_kwargs['position__range'] = min(old_position, new_position), max(old_position, new_position)
        position_kwargs['position'] = Case(
            When(pk=instance.pk, then=Value(new_position)),
            default=F('position') + increment,
            output_field=PositiveIntegerField()
        )

    else:
        filter_kwargs['position__gt'] = instance.position
        position_kwargs['position'] = F('position') - 1

    with transaction.atomic():
        (
            model.objects
            .filter(**filter_kwargs)
            .order_by('position')
            .update(**position_kwargs)
        )
