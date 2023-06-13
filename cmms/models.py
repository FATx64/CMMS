from __future__ import annotations

import datetime as dt
from os import strerror
from typing import TYPE_CHECKING, Type

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from cmms.enums import Periodicity, UserType
from cmms.utils import generate_hexa_id, handle_avatar_upload, snowflake


class UserManager(BaseUserManager):
    if TYPE_CHECKING:
        model: Type[User]

    def _create_user(self, email: str, password: str, **kwargs):
        if not email:
            raise ValueError("Email must be set!")
        email = self.normalize_email(email)
        password = make_password(password)  # type: ignore
        user = self.model(email=email, password=password, **kwargs)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str, **kwargs):
        kwargs.setdefault("type", UserType.ENGINEER)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email: str, password: str, **kwargs):
        kwargs.setdefault("type", UserType.ADMIN)
        return self._create_user(email, password, **kwargs)

    def from_form(self, form_data: dict, **kwargs):
        _type = form_data.get("type", kwargs.get("type"))
        if _type:
            _type = UserType(_type)

        u = self.create_user(
            form_data["email"],
            form_data.get("password", form_data.get("password2")),
            type=_type or UserType.ENGINEER,
        )

        avatar = form_data.get("avatar")
        if avatar:
            avatar = handle_avatar_upload(u.id, avatar)

        e = Employee(
            user=u,
            employee_id=form_data["id"],
            first_name=form_data["first_name"],
            last_name=form_data["last_name"],
            address=form_data["address"],
            phone_number=form_data["phone_number"],
            date_of_birth=form_data["date_of_birth"],
            work_hour=form_data["work_hour"],
            work_place=form_data.get("work_place"),
            avatar=avatar or "",
        )
        e.save(using=self._db)
        return u


class User(AbstractBaseUser):
    """Holds users' auth detail"""

    id: int = models.BigIntegerField(primary_key=True, unique=True)  # type: ignore
    email = models.EmailField(
        unique=True,
        error_messages={
            "unique": "Email is already registered",
        },
    )
    is_active = models.BooleanField(default=True)  # type: ignore
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


class TypedModel(models.Model):
    """models.Model but with better typehint support"""

    if TYPE_CHECKING:
        objects: models.Manager

    class Meta:
        abstract = True


class WorkPlace(TypedModel):
    name = models.CharField(max_length=150)
    code = models.IntegerField()
    location = models.CharField(max_length=150, blank=True)

    def __str__(self) -> str:
        return self.name  # type: ignore

    def employee_count(self) -> int:
        return Employee.objects.filter(work_place=self).count()


class Employee(TypedModel):
    """Holds users' data"""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    employee_id = models.BigIntegerField()
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True, default="")
    phone_number = PhoneNumberField()
    date_of_birth = models.DateField()
    address = models.CharField(max_length=150, blank=True)
    work_hour = models.IntegerField()
    # Empty by default since on first-time setup Work Center is empty
    work_place = models.ForeignKey(WorkPlace, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    avatar = models.CharField(max_length=32, blank=True, default=generate_hexa_id)

    def full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()


class Equipment(TypedModel):
    tag = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    manufacture = models.CharField(max_length=150)
    pm_frequency = models.CharField(max_length=5, choices=Periodicity.choices, default=Periodicity.MONTHLY)
    work_place = models.ForeignKey(WorkPlace, on_delete=models.SET_NULL, blank=True, null=True, default=None)
    cost = models.IntegerField()
    picture = models.CharField(max_length=32, blank=True, default=generate_hexa_id)
    location = models.CharField(max_length=150)
    installation_date = models.DateField()
    warranty_date = models.DateField()
    arrival_date = models.DateField()
    note = models.CharField(max_length=150, blank=True)


class Timer(TypedModel):
    if TYPE_CHECKING:
        name: str
        repeat: int
        repeat_frequency: str
        expires_at: dt.datetime

    name = models.SlugField(max_length=150)  # type: ignore
    # repeat = -1 means it'll repeat forever
    repeat = models.IntegerField(default=0)  # type: ignore
    # if frequency is null or blank, it'll cancel out repeat's value, we'll assume that it only meant to execute once
    repeat_frequency = models.CharField(
        max_length=5, choices=Periodicity.choices, default=Periodicity.MONTHLY, blank=True, null=True
    )  # type: ignore
    expires_at = models.DateField()  # type: ignore
