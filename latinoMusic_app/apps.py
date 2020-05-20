from django.apps import AppConfig


class LatinomusicAppConfig(AppConfig):
    name = 'latinoMusic_app'
    def ready(self):
        import latinoMusic_app.signals
