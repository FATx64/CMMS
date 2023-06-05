#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

from cmms.manage import main as _main
from scripts import MODULE_NAME


def main():
    """Run administrative tasks."""
    root = os.path.join(os.getcwd(), MODULE_NAME)
    sys.path.insert(0, root)
    os.chdir(root)

    _main()  # django's default manage.py


if __name__ == "__main__":
    main()
