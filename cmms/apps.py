import sys

from django.apps import AppConfig
from django.db import models
from graphene import Field
from graphene_django.converter import convert_django_field

from cmms.scalars import BigInt


class CMMSConfig(AppConfig):
    name = "cmms"

    def setup_timer(self):
        if "manage.py" in sys.argv:
            return

        from cmms.timer import Timer

        if "django.core.wsgi" in sys.modules or "django.core.asgi" in sys.modules:
            Timer().start()

    def ready(self):
        self.setup_timer()

        @convert_django_field.register(models.BigIntegerField)
        def convert_field_to_big_int_field(field, registry=None):
            return Field(BigInt, description=field.help_text, required=not field.null)
