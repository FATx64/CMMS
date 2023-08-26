from __future__ import annotations

from typing import TYPE_CHECKING, Collection

from django.conf import settings
from django.http.request import HttpRequest
from django.template import Context

from cmms.core.enums import UserType


if TYPE_CHECKING:
    from cmms.core.models import User


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
        self.context: Context | None = None
        self.request: HttpRequest | None = None
        self.children: Collection[Item] = children
        self.roles: Collection[UserType] = roles

    @property
    def constructed(self):
        return self.context is not None and self.request is not None

    def construct(self, context, request):
        self.context = context
        self.request = request
        return self

    def should_be_shown(self) -> bool:
        if not self.roles:
            return True

        user: User = self.request.user  # type: ignore
        if user.role() == UserType.ADMIN:
            return True
        return user.role() in self.roles

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
