from django.urls import include, path
from rest_framework.routers import SimpleRouter

from src.statement.views import PlayerStatementView
from src.statement.views.queue_view import QueueView

router = SimpleRouter()
router.register(prefix=r'state', viewset=PlayerStatementView, basename='state')
router.register(prefix=r'state', viewset=QueueView, basename='state')

urlpatterns = [
    path('me/', include(router.urls)),
]
