from django import template
from django.http import HttpRequest
from cmms.menu import MenuManager


register = template.Library()


def silence_without_item(fn):
    def wrapped(item, on_yes):
        if not item:
            return ""
        return fn(item, on_yes)

    return wrapped


@register.simple_tag(takes_context=True)
def get_menu(context, request):
    if not isinstance(request, HttpRequest):
        return None
    return MenuManager(context, request)


@register.filter
@silence_without_item
def if_active(item, on_yes):
    print(item)
    print(on_yes)
    return on_yes if item.is_active else ""
