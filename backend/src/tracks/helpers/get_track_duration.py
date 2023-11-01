from audio_metadata import load


def get_track_duration(file) -> int:
    return int(load(file).get('streaminfo').get('duration'))
