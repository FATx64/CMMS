from django.db import models


class UserType(models.TextChoices):
    ENGINEER = "E", "Engineer"
    ADMIN = "A", "Admin"
