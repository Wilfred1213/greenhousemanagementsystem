from django.apps import AppConfig


class SqlappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sqlApp'

    def ready(self):
        import sqlApp.signals
