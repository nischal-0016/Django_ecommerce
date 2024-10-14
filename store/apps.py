from django.apps import AppConfig


class StoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'

class YourAppConfig(AppConfig):
    name = 'your_app'

    def ready(self):
        import your_app.signals