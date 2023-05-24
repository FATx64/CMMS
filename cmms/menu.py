from django.shortcuts import render
from django.conf import settings


class Item:
    def __init__(self, label: str = None, url: str = None, icon: str = None):
        self.label = label
        self.url = url
        # Use Google "Symbols" name. Not "Icons", to avoid future potential breakage
        self.icon = icon or "broken_image"
        self.context = None
        self.request = None

    @property
    def constructed(self):
        return self.context is not None and self.request is not None

    def construct(self, context, request):
        self.context = context
        self.request = request
        return self

    def is_active(self) -> bool:
        if not self.constructed:
            raise RuntimeError
        return self.request.META["PATH_INFO"].rstrip("/") == self.url  # type: ignore


class MenuManager:
    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.items: list[Item] = []
        for i in settings.MENU_ITEMS:
            self.add_item(i)

    def add_item(self, item: Item):
        self.items.append(item.construct(self.context, self.request))
