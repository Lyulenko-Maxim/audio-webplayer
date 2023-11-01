from pathlib import Path
from django.http import FileResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from src.statement.models import PlayerStatement, Queue


class TrackStreamView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, *args, **kwargs):
        current_track = (
            PlayerStatement.objects
            .select_related('context')
            .select_related('context__current_track')
            .filter(user=request.user)
            .only('context__current_track__file')
            .first()
        ).context.current_track

        if not current_track:
            return Response(data={'message': 'Очередь пуста.'}, status=status.HTTP_204_NO_CONTENT)

        current_track.plays += 1
        current_track.save()
        path = Path(current_track.file.path)
        file = path.open(mode='rb')
        content_length = path.stat().st_size

        response = FileResponse(
            streaming_content=file,
            as_attachment=False,
            headers={
                'Accept-Ranges': 'bytes',
                'Content-Length': content_length,
                'Cache-Control': 'no-cache',
            },
        )
        response.block_size = 4024
        return response
