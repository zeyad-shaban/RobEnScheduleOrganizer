from django.apps import AppConfig

class SchedualeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "schedule"

    def ready(self):
        import schedule.signals
