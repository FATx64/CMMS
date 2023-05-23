from django.conf import settings


class Item:
    def __init__(self, label: str = None, url: str = None):
        self.label = label
        self.url = url
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
        return self.url in self.request.META["PATH_INFO"]  # type: ignore


class MenuManager:
    def __init__(self, context, request):
        self.context = context
        self.request = request

        self.items: list[Item] = []
        for i in settings.MENU_ITEMS:
            self.add_item(i)

    def add_item(self, item: Item):
        self.items.append(item.construct(self.context, self.request))
