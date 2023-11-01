from django.urls import include, path
from rest_framework.routers import SimpleRouter

from src.playlists.views import PlaylistReadOnlyView, PlaylistView

router = SimpleRouter()
router.register(prefix='me/playlists', viewset=PlaylistView)
router.register(prefix='playlists', viewset=PlaylistReadOnlyView)

urlpatterns = [
    path('', include(router.urls)),
]
