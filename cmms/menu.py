from __future__ import annotations

from typing import Collection

from django.conf import settings

from cmms.enums import UserType


class ItemNotConstructed(RuntimeError):
    def __init__(self):
        super().__init__("Item is not yet constructed!")


class Item:
    def __init__(
        self,
        label: str,
        url: str,
        icon: str | None = None,
        *,
        children: Collection[Item] = [],
        roles: Collection[UserType] = [],
    ):
        self.label: str = label
        self.url: str = url
        # Use Google "Symbols" name. Not "Icons", to avoid future potential breakage
        self.icon: str = icon or "broken_image"
        self.context = None
        self.request = None
        self.children: Collection[Item] = children
        self.roles: Collection[UserType] = roles

    @property
    def constructed(self):
        return self.context is not None and self.request is not None

    def construct(self, context, request):
        self.context = context
        self.request = request
        return self

    def is_active(self) -> bool:
        if not self.constructed:
            raise ItemNotConstructed
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
