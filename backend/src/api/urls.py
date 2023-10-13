from django.urls import include, path

urlpatterns = [
    path('v1/', include('src.music.v1_urls')),
    path('v1/auth/', include('src.oauth.v1_urls')),
]
