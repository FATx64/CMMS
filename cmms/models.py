from typing import TYPE_CHECKING
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from cmms.enums import UserType
from cmms.utils import snowflake


class UserManager(BaseUserManager):
    def _create_user(self, email: str, password: str, **kwargs):
        if not email:
            raise ValueError("Email must be set!")
        email = self.normalize_email(email)
        password = make_password(password)
        user = self.model(email=email, password=password, **kwargs)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **kwargs):
        kwargs.setdefault("type", UserType.ENGINEER)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email: str, password: str, **kwargs):
        kwargs.setdefault("type", UserType.ADMIN)
        return self._create_user(email, password, **kwargs)

    def superuser_form(self, form_data: dict):
        u = self.create_superuser(form_data["email"], form_data["password2"])
        e = Employee(
            user=u,
            employee_id=form_data["id"],
            first_name=form_data["first_name"],
            last_name=form_data["last_name"],
            address=form_data["address"],
            phone_number=form_data["phone_number"],
            work_hour=form_data["work_hour"],
            avatar="",
        )
        e.save(using=self._db)
        return u


class User(AbstractBaseUser):
    """Holds users' auth detail"""

    id = models.BigIntegerField(primary_key=True, unique=True)
    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "Email is already registered",
        },
    )
    is_active = models.BooleanField(default=True)
    type = models.CharField(max_length=5, choices=UserType.choices)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    def is_admin(self):
        return self.type == UserType.ADMIN

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = snowflake()
        super().save(*args, **kwargs)

    def role(self):
        return UserType(self.type)


class WorkPlace(models.Model):
    if TYPE_CHECKING:
        objects: models.Manager

    name = models.CharField(max_length=150)
    code = models.IntegerField()
    location = models.CharField(max_length=150, blank=True)


class Employee(models.Model):
    """Holds users' data"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    employee_id = models.BigIntegerField()
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True, default="")
    phone_number = PhoneNumberField()
    address = models.CharField(max_length=150, blank=True)
    work_hour = models.IntegerField()
    # Empty by default since on first-time setup Work Center is empty
    work_place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE, blank=True, null=True, default=None)
    avatar = models.CharField(max_length=32, blank=True, default="")  # utils.generate_hexa_id()

    def full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
