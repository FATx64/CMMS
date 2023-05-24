import datetime
import random
import uuid


CMMS_EPOCH: int = 1672531200000


def utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def snowflake(dt: datetime.datetime = None, /, *, high: bool = False) -> int:
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
