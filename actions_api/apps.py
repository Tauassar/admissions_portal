from django.apps import AppConfig


class ActionsApiConfig(AppConfig):
    name = 'actions_api'

    def ready(self):
        import actions_api.signals