from django.db import models


class UserType(models.TextChoices):
    ADMIN = "A", "Admin"
    ENGINEER = "E", "Engineer"
