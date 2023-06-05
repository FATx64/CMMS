"""
Mainly for poetry

REF: https://github.com/kanu/django-poetry-example/blob/978dae3/scripts.py
"""

import os
import sys

from django.core.management import execute_from_command_line


MODULE_NAME = "cmms"


def _execute(*sys_args):
    """fiddles around with the sys and os.path before calling the django command."""
    root = os.path.join(os.getcwd(), MODULE_NAME)
    sys.path.insert(0, root)
    os.chdir(root)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cmms.settings")
    sys.argv = sys_args
    execute_from_command_line(sys.argv)


def runserver():
    _execute("manage.py", "runserver", "8000")


def tailwind():
    _execute("manage.py", "tailwind", "start")


def manage():
    _execute("manage.py", *sys.argv[1:])
