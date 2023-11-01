from src.tracks.helpers import get_track_duration


def set_track_serializer_duration(serializer):
    serializer.validated_data['duration'] = get_track_duration(
        serializer.validated_data.get('file').temporary_file_path()
    )
    return serializer
