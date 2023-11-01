from django.urls import include, path
from rest_framework.routers import SimpleRouter

from src.tracks.views import TrackReadOnlyView, TrackStreamView, TrackView

router = SimpleRouter()
router.register(prefix='tracks', viewset=TrackReadOnlyView)
router.register(prefix='me/tracks', viewset=TrackView)

urlpatterns = [
    path('', include(router.urls)),
    path('me/stream/', TrackStreamView.as_view(), name='stream'),
]
