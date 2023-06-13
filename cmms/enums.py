from django.db import models


class UserType(models.TextChoices):
    ENGINEER = "E", "Engineer"
    ADMIN = "A", "Admin"


class Periodicity(models.TextChoices):
    MONTHLY = "M", "Monthly"
    WEEKLY = "W", "Weekly"
    DAILY = "D", "Daily"
    NEVER = "N", "Never"


class WorkOrderType(models.TextChoices):
    PM = "PM", "Preventive Maintenance"
    CM = "CM", "Corrective Maintenance"
