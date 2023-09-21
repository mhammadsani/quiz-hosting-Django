from django.apps import AppConfig


class QuizAttempterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quiz_management'

    def ready(self) -> None:
        import quiz_management.signals