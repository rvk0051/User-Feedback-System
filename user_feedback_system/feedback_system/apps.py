from django.apps import AppConfig


class FeedbackSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'feedback_system'

    def ready(self):
        # This will ensure that the templatetags are loaded

        from .templatetags import feedback_tags
        from . import signals

