from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import user_passes_test

from cmms.enums import UserType
from cmms.models import User


def admin_exists(*args):
    def func(*_):
        return len(User.objects.filter(type=UserType.ADMIN)) > 0

    return user_passes_test(func, login_url="/setup")(*args)


def admin_not_exists(view_func):
    @wraps(view_func)
    def _wrapper_view(request, *args, **kwargs):
        if len(User.objects.filter(type=UserType.ADMIN)) <= 0:
            return view_func(request, *args, **kwargs)
        return redirect("/")

    return _wrapper_view
