from rest_framework.routers import SimpleRouter

from src.albums.views import AlbumReadOnlyView, AlbumView

router = SimpleRouter()
router.register(prefix='albums', viewset=AlbumReadOnlyView)
router.register(prefix='me/albums', viewset=AlbumView)

urlpatterns = router.urls
