from django.urls import include, path

urlpatterns = [
    path('v1/', include('src.albums.v1_urls')),
    path('v1/', include('src.tracks.v1_urls')),
    path('v1/', include('src.playlists.v1_urls')),
    path('v1/', include('src.statement.v1_urls')),
    path('v1/', include('src.search.v1_urls')),
    path('v1/', include('src.users.v1_urls')),
    path('v1/', include('src.artists.v1_urls')),
    path('v1/', include('src.authentication.v1_urls')),
    path('v1/', include('src.metadata.v1_urls')),
]
