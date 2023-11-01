from django.core.cache import cache
from django.db.models import Case, Prefetch, When
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from src.statement.models import PlayerStatement, Queue
from src.statement.serializers import QueueSerializer
from src.tracks.models import Track


class QueueView(GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='queue', serializer_class=QueueSerializer)
    def get_queue(self, request):
        user = request.user
        statement = get_object_or_404(PlayerStatement, user=user)
        tracks_queryset = Track.objects.all()

        if statement.is_shuffle:
            cache_key = f'user_queue_positions_{user.pk}'
            shuffled_positions = cache.get(cache_key)
            conditions = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(shuffled_positions)])
            tracks_queryset = Track.objects.alias(conditions=conditions).order_by('conditions')

        queue = get_object_or_404(
            Queue.objects.prefetch_related(
                Prefetch(lookup='tracks', queryset=tracks_queryset)
            ),
            user=user
        )

        serializer = self.get_serializer(queue)
        return Response(serializer.data)
