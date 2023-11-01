from django.apps import AppConfig


class StatementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.statement'

    def ready(self):
        from . import signals
