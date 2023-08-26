"""
WSGI config for cmms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from cmms import constants


os.environ.setdefault("DJANGO_SETTINGS_MODULE", constants.DJANGO_SETTINGS_PATH)

application = get_wsgi_application()
