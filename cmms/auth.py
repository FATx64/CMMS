from __future__ import annotations

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model


class CMMSBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        User = get_user_model()
        user = User.objects.get(email=email)
        if user:
            pwd = check_password(password, user.password)
            return user if pwd else None
        return None


    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
