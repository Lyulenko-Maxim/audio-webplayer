from django.urls import path

from src.oauth.views import LoginView, RegisterView, UserListView

urlpatterns = [
    path('register/', RegisterView.as_view(), name = 'register'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('users/', UserListView.as_view())
]
