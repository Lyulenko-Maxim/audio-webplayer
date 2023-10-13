from src.music.models import Collaboration, Track
from src.users.models import Artist


def create_collaborations(track: Track, artists: list[int] | int = None):
    """Записывает артистов в коллаборацию (если они есть)."""

    if not artists:
        return

    collaborations = []

    for artist_id in artists:
        try:
            artist = Artist.objects.get(id = artist_id)
        except Artist.DoesNotExist:
            pass
        else:
            collaboration = Collaboration(track = track, artist = artist)
            collaborations.append(collaboration)

    Collaboration.objects.bulk_create(objs = collaborations)
