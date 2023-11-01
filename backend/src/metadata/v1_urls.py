from django.urls import include, path
from src.metadata.views import get_countries

urlpatterns = [
    path('metadata/countries/', get_countries, name='countries'),
]
