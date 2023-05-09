from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from cmms.enums import UserType


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **kwargs):
        if not email:
            raise ValueError("Email must be set!")
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **kwargs)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **kwargs):
        kwargs.setdefault("is_admin", False)
        return self.create_user(email, password, **kwargs)

    def create_superuser(self, email: str, password: str, **kwargs):
        kwargs.setdefault("is_admin", True)
        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser):
    """Holds users' auth detail"""

    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "Email is already registered",
        },
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False, help_text="Whether user have the highest permission on CMMS")

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"


class Employee(models.Model):
    """Holds users' data"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    employee_id = models.BigIntegerField()
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=150, blank=True)
    work_hour = models.TimeField()
    work_place = models.CharField(max_length=150, blank=True)

    def get_full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
