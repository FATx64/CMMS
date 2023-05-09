from django.db import models


class UserType(models.TextChoices):
    ADMIN = "A"
    ENGINEER = "E"
