from functools import wraps

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

from cmms.core.models import User
from cmms.core.enums import UserType


def admin_exists(view_func):
    @wraps(view_func)
    def _wrapper_view(request, *args, **kwargs):
        exists = len(User.objects.filter(type=UserType.ADMIN)) > 0

        if exists:
            return view_func(request, *args, **kwargs)
        return redirect("/setup")

    return _wrapper_view


def admin_not_exists(view_func):
    @wraps(view_func)
    def _wrapper_view(request, *args, **kwargs):
        exists = len(User.objects.filter(type=UserType.ADMIN)) > 0

        if not exists:
            return view_func(request, *args, **kwargs)
        return redirect("/")

    return _wrapper_view
