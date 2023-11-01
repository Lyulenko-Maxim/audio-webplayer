import django_filters

from src.artists.models import Artist


class ArtistFilter(django_filters.FilterSet):
    stage_name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Artist
        fields = ('stage_name',)
