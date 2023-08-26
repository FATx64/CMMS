"""
ASGI config for cmms project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from cmms import constants


os.environ.setdefault("DJANGO_SETTINGS_MODULE", constants.DJANGO_SETTINGS_PATH)

application = get_asgi_application()
