from django.urls import include, path

from src.music.views import CreateAlbumView

urlpatterns = [
    path('album/', CreateAlbumView.as_view()),
]
