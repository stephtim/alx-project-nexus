from django.apps import AppConfig

class StoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "store"

    def ready(self):
        # import signals to register them
        try:
            import store.signals  # noqa
        except Exception:
            pass
