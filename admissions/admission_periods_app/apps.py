from django.apps import AppConfig


class AdmissionPeriodsAppConfig(AppConfig):
    name = 'admission_periods_app'

    def ready(self):
        import admission_periods_app.signals
