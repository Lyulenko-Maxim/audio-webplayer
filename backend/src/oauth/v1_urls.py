from django.urls import path

from src.oauth.views import ListenerSignUpView, SignInView, ArtistSignUpView

urlpatterns = [
    path('sign-up/listener/', ListenerSignUpView.as_view(), name='listener-sign-up'),
    path('sign-up/artist/', ArtistSignUpView.as_view(), name='artist-sign-up'),
    path('sign-in/', SignInView.as_view(), name='sign-in'),

]
