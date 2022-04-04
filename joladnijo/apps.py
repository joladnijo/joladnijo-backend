from django.apps import AppConfig


class JoladnijoConfig(AppConfig):
    name = 'joladnijo'
    verbose_name = 'Jól adni jó'

    def ready(self):
        import joladnijo.signals  # noqa: F401
