from django.urls import include, path
from rest_framework.routers import SimpleRouter

from src.users.views import UserProfileReadOnlyView, UserProfileView

router = SimpleRouter()
router.register(prefix=r'me', viewset=UserProfileView)
router.register(prefix=r'users', viewset=UserProfileReadOnlyView)
urlpatterns = [
    path('', include(router.urls)),
]
