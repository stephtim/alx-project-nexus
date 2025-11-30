from django.apps import AppConfig

class EcommerceConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "ecommerce"

    def ready(self):
        # import signals
        try:
            import ecommerce.signals  # noqa
        except Exception:
            pass
