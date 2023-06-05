from django import template
from django.http import HttpRequest

from cmms.menu import Item, MenuManager


register = template.Library()


def silence_without_item(fn):
    def wrapped(item, pair):
        if not isinstance(item, Item):
            raise RuntimeError("The value of item is not instance of Item!")
        return fn(item, pair)

    return wrapped


@register.simple_tag(takes_context=True)
def get_menu(context, request):
    if not isinstance(request, HttpRequest):
        return None
    return MenuManager(context, request)


@register.filter("if_active")
@silence_without_item
def if_active(item, pair):
    s = pair.split("|")
    on_true = s[0]
    try:
        on_false = s[1]
    except IndexError:
        on_false = ""

    return on_true if item.is_active() else on_false
