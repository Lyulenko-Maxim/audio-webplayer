import django_filters

from src.albums.models import Album


class AlbumFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Album
        fields = ('title',)
