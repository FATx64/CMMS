from __future__ import annotations

import datetime
import io
import random
import uuid
from pathlib import Path
from typing import TYPE_CHECKING, Any

from django.conf import settings
from django.core.files.base import File
from django.core.files.uploadedfile import UploadedFile
from django.forms.utils import flatatt
from django.forms.widgets import static
from django.http.request import HttpRequest
from django.utils.html import format_html, html_safe, mark_safe
from PIL import Image

from cmms import models
from cmms.events import Events


CMMS_EPOCH: int = 1672531200000


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def snowflake(dt: datetime.datetime | None = None, /, *, high: bool = False) -> int:
    """Simplified version of how discord ID generated

    REF: https://github.com/Rapptz/discord.py/blob/e870bb1335e3f824c83a40df4ea9b17f215fde63/discord/utils.py#L395-L422
    """
    if not dt:
        dt = utcnow()
    millis = int(dt.timestamp() * 1000 - CMMS_EPOCH)
    return (millis << 22) + (2**22 - 1 if high else 0) + random.randint(0, 10)


def time_from_snowflake(id: int, /) -> datetime.datetime:
    """REF: https://github.com/Rapptz/discord.py/blob/e870bb1335e3f824c83a40df4ea9b17f215fde63/discord/utils.py#L375-L392"""
    millis = ((id >> 22) + CMMS_EPOCH) / 1000
    return datetime.datetime.fromtimestamp(millis, tz=datetime.timezone.utc)


def generate_hexa_id() -> str:
    """Generate 32 long hexa id"""
    return uuid.uuid1().hex


def handle_image_upload(path: Path, file: UploadedFile) -> str:
    _id = generate_hexa_id()
    path.mkdir(parents=True, exist_ok=True)

    buffer = io.BytesIO()
    for chunk in File(file):
        buffer.write(chunk)

    buffer.seek(0)
    img = Image.open(buffer)
    img.save(path / f"{_id}.webp", "WEBP")
    return _id


def handle_avatar_upload(user_id: int, file: UploadedFile) -> str:
    return handle_image_upload(Path(f"data/avatars/{user_id}"), file)


def handle_equipment_pict_upload(equipment_id: int, file: UploadedFile) -> str:
    print(equipment_id)
    return handle_image_upload(Path(f"data/pictures/{equipment_id}"), file)


@html_safe
class JS:
    def __init__(self, js: str | None, attrs: dict[str, Any] | None = None):
        self.js = js
        self.attrs = attrs or {}

    def __str__(self):
        if self.js is None:
            return format_html("<script {}></script>", mark_safe(flatatt(self.attrs)))
        return format_html(
            '<script src="{}"{}></script>',
            self.js if self.js.startswith(("http://", "https://", "/")) else static(self.js),
            mark_safe(flatatt(self.attrs)),
        )


class CMMSRequest(HttpRequest):
    if TYPE_CHECKING:
        user: models.User
