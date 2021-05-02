from django.apps import AppConfig


class CandidatesAppConfig(AppConfig):
    name = 'candidates_app'

    def ready(self):
        import candidates_app.signals