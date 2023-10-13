from src.music.models import Track


def create_track(track_data: dict) -> Track:
    """Создает трек и привязывает его к текущему артисту."""

    artist = track_data['artist']
    track = artist.tracks.create(**track_data)

    return track
