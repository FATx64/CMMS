from django.db import models


class UserType(models.TextChoices):
    ENGINEER = "E", "Engineer"
    ADMIN = "A", "Admin"


class Periodicity(models.TextChoices):
    MONTHLY = "M", "Monthly"
    WEEKLY = "W", "Weekly"
    DAILY = "D", "Daily"
    HOURLY = "H", "Hourly"
    NEVER = "N", "Never"

    @staticmethod
    def to_dt_kwargs(keyword: str, time: int) -> dict[str, int]:
        kwargs = {}
        key = None
        match keyword:
            case Periodicity.MONTHLY:
                key = "months"
            case Periodicity.WEEKLY:
                key = "weeks"
            case Periodicity.DAILY:
                key = "days"
            case Periodicity.HOURLY:
                key = "hours"
            case None | Periodicity.NEVER:
                key = None

        if not key:
            return kwargs

        kwargs[key] = time
        return kwargs


class WorkOrderType(models.TextChoices):
    PM = "PM", "Preventive Maintenance"
    CM = "CM", "Corrective Maintenance"
