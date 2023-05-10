from django.contrib.auth.decorators import user_passes_test

from cmms.enums import UserType
from cmms.models import User


def admin_exists(*args):
    def func(*_):
        return len(User.objects.filter(type=UserType.ADMIN)) > 0

    return user_passes_test(func, login_url="/setup")(*args)
