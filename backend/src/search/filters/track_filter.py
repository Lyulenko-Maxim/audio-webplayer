import django_filters

from src.tracks.models import Track


class TrackFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Track
        fields = ('title',)
