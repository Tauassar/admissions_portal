from django.apps import AppConfig


class EvaluationsAppConfig(AppConfig):
    name = 'evaluations_app'

    def ready(self):
        import evaluations_app.signals