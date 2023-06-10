from django.db import models


class UserType(models.TextChoices):
    ENGINEER = "E", "Engineer"
    ADMIN = "A", "Admin"


class Periodicity(models.TextChoices):
    DAILY = "D", "Daily"
    WEEKLY = "W", "Weekly"
    MONTHLY = "M", "Monthly"
    NEVER = "N", "Never"