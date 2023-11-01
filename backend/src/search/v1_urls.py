from django.urls import path

from src.search.views import SearchView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
]
