from __future__ import annotations

from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from cmms.models import User


class CMMSBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None) -> User | None:
        user = User.objects.get(email=email)
        if user:
            pwd = check_password(password, user.password)
            return user if pwd else None
        return None
