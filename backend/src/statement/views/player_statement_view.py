import random

from django.core.cache import cache
from django.db import transaction
from django.db.models import Case, Count, Prefetch, When
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.albums.models import Album
from src.playlists.models import Playlist
from src.statement.models import AlbumContext, Context, PlaylistContext, Queue
from src.statement.models.player_statement import PlayerStatement
from src.statement.serializers.player_statement_serializer import (
    PlayerStatementSerializer,
    IsPlayingStateSerializer,
    VolumeStateSerializer,
    CurrentPositionStateSerializer,
    ShuffleStateSerializer,
    RepeatStateSerializer,
    ContextStateSerializer,
)
from src.tracks.models import Track


class PlayerStatementView(viewsets.GenericViewSet):
    serializer_class = PlayerStatementSerializer
    permission_classes = [IsAuthenticated]

    def get_validated_statement(self, request):
        statement = get_object_or_404(PlayerStatement, user=request.user)
        serializer = self.get_serializer(statement, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        return statement, serializer

    def list(self, request):
        statement = get_object_or_404(PlayerStatement, user=request.user)
        serializer = self.get_serializer(statement)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def save(self, request):
        _, serializer = self.get_validated_statement(request)
        serializer.save()
        return Response(data={"message": 'Воспроизведение включено.'})

    @action(detail=False, methods=['post'], url_path='play', serializer_class=IsPlayingStateSerializer)
    def set_play(self, request):
        statement = get_object_or_404(PlayerStatement, user=request.user)
        if not statement.is_playing:
            statement.is_playing = True
            statement.save()
        return Response(data={"message": 'Воспроизведение включено.'})

    @action(detail=False, methods=['post'], url_path='pause', serializer_class=IsPlayingStateSerializer)
    def set_pause(self, request):
        statement = get_object_or_404(PlayerStatement, user=request.user)
        if statement.is_playing:
            statement.is_playing = False
            statement.save()
        return Response(data={"message": 'Воспроизведение приостановлено.'})

    @action(detail=False, methods=['put'], url_path='volume', serializer_class=VolumeStateSerializer)
    def set_volume(self, request):
        statement, serializer = self.get_validated_statement(request)
        volume = serializer.validated_data['volume']
        if statement.volume != volume:
            statement.volume = volume
            statement.save()

        return Response(data={"message": f'Установлена громкость {volume * 100}%.'})

    @action(detail=False, methods=['put'], url_path='seek', serializer_class=CurrentPositionStateSerializer)
    def set_current_position(self, request):
        statement, serializer = self.get_validated_statement(request)
        current_position = serializer.validated_data['current_position']
        statement.current_position = current_position
        statement.save()
        return Response(data={"message": f'Установлена позиция воспроизведения в {current_position} секунд.'})

    @action(detail=False, methods=['post'], url_path='shuffle', serializer_class=ShuffleStateSerializer)
    def toggle_shuffle(self, request):
        user = request.user
        statement = get_object_or_404(PlayerStatement, user=user)
        is_shuffle = not statement.is_shuffle
        statement.is_shuffle = is_shuffle
        statement.save()

        cache_key = f'user_queue_positions_{user.pk}'

        if not is_shuffle:
            cache.delete(cache_key)
            return Response(data={"message": 'Случайный порядок выключен.'})

        queue = get_object_or_404(
            Queue.objects.annotate(total_tracks=Count('tracks')),
            user=user
        )

        positions = [track.pk for track in queue.tracks.all()]
        random.shuffle(positions)

        cache.set(cache_key, positions)

        return Response(data={"message": 'Случайный порядок включен.'})

    @action(detail=False, methods=['put'], url_path='context', serializer_class=ContextStateSerializer)
    def set_context(self, request):
        user = request.user
        statement = get_object_or_404(
            queryset=(
                PlayerStatement.objects
                .select_related('context')
            ),
            user=user
        )
        serializer = self.get_serializer(statement, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        context = serializer.validated_data.get('context', None)

        if not context:
            statement.context = None
            statement.save()
            return Response({"message": 'Установлен пустой контекст.'})

        context_type = context.get('type', None)
        context_id = context.get('context_id', None)
        current_track = context.get('current_track', None)
        track_queryset = None
        if current_track:
            track_queryset = get_object_or_404(Track, pk=current_track.pk)

        if current_track and not context_type:
            context, created = Context.objects.get_or_create(
                current_track=current_track,
                defaults={'current_track': current_track}
            )

            context.save()
            statement.context = context

            statement.context.type = context_type
            statement.context.context_id = context_id
            statement.context.current_track = current_track
            statement.save()

            queue = get_object_or_404(
                Queue.objects
                .prefetch_related('tracks'),
                user=request.user
            )
            queue.tracks.set([current_track])
            return Response({"message": 'Установлен пустой контекст и текущий трек.'})

        elif not current_track and not context_type:
            statement.context = None
            statement.save()
            queue = get_object_or_404(
                Queue.objects
                .prefetch_related('tracks'),
                user=request.user
            )
            queue.tracks.set([])
            return Response({"message": 'Установлен пустой контекст.'})

        context_mapping = {
            'album': {
                'response_message': 'Установлен контекст альбома.',
            },
            'playlist': {
                'response_message': 'Установлен контекст плейлиста.',
            },
        }

        context_map = context_mapping.get(context_type)

        if not context_map:
            return Response(data={"error": 'Недопустимый тип контекста.'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            context, created = Context.objects.get_or_create(
                context_id=context_id,
                type=context_type,
                current_track=current_track
            )

            context.save()
            statement.context = context

            statement.context.type = context_type
            statement.context.context_id = context_id
            statement.context.current_track = track_queryset
            statement.save()

            queue = get_object_or_404(
                Queue.objects
                .prefetch_related('tracks'),
                user=request.user
            )

            if context_type == 'album':
                tracks = Track.objects.filter(album_id=context_id)
            elif context_type == 'playlist':
                tracks = Playlist.objects.prefetch_related('tracks').get(pk=context_id).tracks
            else:
                tracks = current_track
            queue.tracks.set(tracks)
            queue.save()

        return Response(data={"message": context_map.get('response_message')})

    @action(detail=False, methods=['put'], url_path='repeat', serializer_class=RepeatStateSerializer)
    def toggle_repeat_mode(self, request):
        user = request.user
        statement = get_object_or_404(PlayerStatement, user=user)
        serializer = self.get_serializer(statement, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        repeat_mode = serializer.validated_data['repeat_state']
        serializer.save()

        return Response({'message': f'Режим повтора изменен на "{repeat_mode}".'})

    @action(detail=False, methods=['post'], url_path='next', serializer_class=IsPlayingStateSerializer)
    def skip_to_next(self, request):
        user = request.user
        statement = get_object_or_404(PlayerStatement.objects.select_related('context__current_track'), user=user)
        is_shuffle = statement.is_shuffle
        repeat_mode = statement.repeat_state
        tracks_queryset = Track.objects.all()
        shuffled_positions = None

        if is_shuffle:
            cache_key = f'user_queue_positions_{user.pk}'
            shuffled_positions = cache.get(cache_key)
            conditions = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(shuffled_positions)])
            tracks_queryset = Track.objects.alias(conditions=conditions).order_by('conditions')

        queue = get_object_or_404(
            Queue.objects
            .prefetch_related(
                Prefetch(lookup='tracks', queryset=tracks_queryset)
            ), user=user
        )

        tracks = queue.tracks

        if not tracks:
            return Response(data={'message': 'Очередь пуста.'}, status=status.HTTP_204_NO_CONTENT)

        current_track = statement.context.current_track
        next_track = None

        if not current_track:
            next_track = tracks.first()

        elif repeat_mode == 'track':
            next_track = current_track

        elif (repeat_mode == 'context'
              and is_shuffle
              and shuffled_positions.index(current_track.pk) == len(shuffled_positions) - 1):
            next_track = tracks.first()

        elif (repeat_mode == 'context'
              and not is_shuffle
              and current_track.pk == tracks.last().pk):
            next_track = tracks.first()

        elif is_shuffle and shuffled_positions.index(current_track.pk) != len(shuffled_positions) - 1:
            current_track_index = shuffled_positions.index(current_track.pk)
            next_track_pk = shuffled_positions[current_track_index + 1]
            next_track = tracks.filter(pk=next_track_pk).first()

        elif not is_shuffle:
            next_track = tracks.filter(pk__gt=tracks.get(pk=current_track.id).id).first()

        if next_track:
            statement.context.current_track = next_track
            statement.context.save()
            statement.save()
            return Response({'message': 'Установлен следующий трек'})

        return Response(data={'message': 'Нет следующего трека.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['post'], url_path='prev', serializer_class=IsPlayingStateSerializer)
    def skip_to_previous(self, request):
        user = request.user
        statement = get_object_or_404(PlayerStatement.objects.select_related('context__current_track'), user=user)
        is_shuffle = statement.is_shuffle
        repeat_mode = statement.repeat_state
        tracks_queryset = Track.objects.all()
        shuffled_positions = None

        if is_shuffle:
            cache_key = f'user_queue_positions_{user.pk}'
            shuffled_positions = cache.get(cache_key)
            conditions = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(shuffled_positions)])
            tracks_queryset = Track.objects.alias(conditions=conditions).order_by('conditions')

        queue = get_object_or_404(
            Queue.objects
            .prefetch_related(
                Prefetch(lookup='tracks', queryset=tracks_queryset)
            ), user=user
        )

        tracks = queue.tracks

        if not tracks:
            return Response(data={'message': 'Очередь пуста.'}, status=status.HTTP_204_NO_CONTENT)

        current_track = statement.context.current_track
        prev_track = None

        if not current_track:
            prev_track = tracks.last()

        elif repeat_mode == 'track':
            prev_track = current_track

        elif (repeat_mode == 'context'
              and is_shuffle
              and shuffled_positions.index(current_track.pk) == 0):
            prev_track = tracks.last()

        elif (repeat_mode == 'context'
              and not is_shuffle
              and current_track.pk == tracks.first().pk):
            prev_track = tracks.last()

        elif is_shuffle and shuffled_positions.index(current_track.pk) != 0:
            current_track_index = shuffled_positions.index(current_track.pk)
            prev_track_pk = shuffled_positions[current_track_index - 1]
            prev_track = tracks.filter(pk=prev_track_pk).first()

        elif not is_shuffle:
            prev_track = tracks.filter(pk__lt=tracks.get(pk=current_track.id).id).last()

        if prev_track:
            statement.context.current_track = prev_track
            statement.context.save()
            statement.save()
            return Response({'message': 'Установлен предыдущий трек'})

        return Response(data={'message': 'Нет предыдущего трека.'}, status=status.HTTP_204_NO_CONTENT)
