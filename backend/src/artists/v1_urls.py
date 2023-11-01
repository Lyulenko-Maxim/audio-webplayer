from django.urls import include, path
from rest_framework.routers import SimpleRouter

from src.artists.views.artist_read_only_view import ArtistReadOnlyView
from src.artists.views.artist_view import ArtistView

router = SimpleRouter()
router.register(prefix='me/artist', viewset=ArtistView)
router.register(prefix='artists', viewset=ArtistReadOnlyView)

urlpatterns = [
    path('', include(router.urls)),
]
