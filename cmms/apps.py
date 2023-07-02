import sys

from django.apps import AppConfig


class CMMSConfig(AppConfig):
    name = "cmms"

    def ready(self):
        if "manage.py" in sys.argv:
            return

        from cmms.timer import Timer

        if "django.core.wsgi" in sys.modules or "django.core.asgi" in sys.modules:
            Timer().start()
