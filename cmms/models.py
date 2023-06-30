from __future__ import annotations

import datetime as dt
import json
from typing import TYPE_CHECKING, Any, Type

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.core import serializers
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from cmms import constants, timer
from cmms.enums import Periodicity, UserType, WorkOrderType
from cmms.utils import (
    generate_hexa_id,
    handle_avatar_upload,
    handle_equipment_pict_upload,
    snowflake,
    utcnow,
)


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


class EquipmentManager(models.Manager):
    def create(
        self,
        tag,
        name,
        manufacture,
        pm_frequency: Periodicity,
        work_place,
        cost,
        location,
        installation_date,
        warranty_date,
        arrival_date,
        note,
        **kwargs,
    ) -> Equipment:
        e = Equipment(
            tag=tag,
            name=name,
            manufacture=manufacture,
            pm_frequency=pm_frequency,
            work_place=work_place,
            cost=cost,
            location=location,
            installation_date=installation_date,
            warranty_date=warranty_date,
            arrival_date=arrival_date,
            note=note,
        )
        e.save()
        picture = kwargs.get("picture")
        if picture:
            pict = handle_equipment_pict_upload(e.id, picture)
            if pict:
                e.picture = pict  # type: ignore [reportGeneralTypeIssues]
                e.save()

        self.create_timer(pm_frequency, e.id)

        return e

    def edit(
        self,
        id,
        tag,
        name,
        manufacture,
        pm_frequency: Periodicity,
        work_place,
        cost,
        location,
        installation_date,
        warranty_date,
        arrival_date,
        note,
        **kwargs,
    ) -> Equipment:
        filter = Equipment.objects.filter(pk=id)
        filter.update(
            tag=tag,
            name=name,
            manufacture=manufacture,
            pm_frequency=pm_frequency,
            work_place=work_place,
            cost=cost,
            location=location,
            installation_date=installation_date,
            warranty_date=warranty_date,
            arrival_date=arrival_date,
            note=note,
        )

        picture = kwargs.get("picture")
        if picture:
            pict = handle_equipment_pict_upload(id, picture)
            if pict:
                filter.update(picture=pict)

        t = Timer.objects.delete(extra={"kwargs": {"equipment_id": id}})
        if t is not None:
            self.create_timer(pm_frequency, id)

        return Equipment.objects.get(pk=id)

    def create_timer(
        self,
        frequency: Periodicity,
        equipment_id,
    ) -> None:
        if not frequency or frequency == Periodicity.NEVER:
            return

        timer_expiry_date = utcnow()
        if frequency == Periodicity.MONTHLY:
            timer_expiry_date -= dt.timedelta(weeks=1)
        timer_expiry_date += relativedelta(**Periodicity.to_dt_kwargs(frequency, 1))  # type: ignore

        Timer.objects.create(
            constants.SCHEDULED_PM,
            -1,
            frequency,
            timer_expiry_date,
            {"kwargs": {"equipment_id": equipment_id}},
        )


class TimerManager(models.Manager):
    def create(
        self,
        name: str,
        repeat: int,
        repeat_frequency: Periodicity,
        expires_at: dt.datetime,
        extra: dict[str, Any],
    ) -> Timer:
        t = Timer(name=name, repeat=repeat, repeat_frequency=repeat_frequency, expires_at=expires_at, extra=extra)
        t.save()
        timer.Timer().restart()
        return t

    def delete(self, **filter):
        t = Timer.objects.get(**filter)
        rt = None
        if t:
            rt = t.delete()
        timer.Timer().restart()
        return rt


class WorkOrderManager(models.Manager):
    def create(
        self,
        type: WorkOrderType,
        description: str,
        start_date: dt.datetime,
        end_date: dt.datetime,
        equipment: Equipment,
    ) -> WorkOrder:
        last = WorkOrder.objects.filter(type=type).order_by("code").last()

        wo = WorkOrder(
            type=type,
            code=last.code + 1 if last else 0,
            description=description,
            start_date=start_date,
            end_date=end_date,
            equipment=equipment,
        )
        wo.save()
        return wo


class User(AbstractBaseUser):
    """Holds users' auth detail"""

    if TYPE_CHECKING:
        employee: Employee

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

    def as_json(self):
        base = {"id": self.pk}
        base["email"] = self.email
        base["type"] = self.type
        employee = self.employee.as_json()
        base["employee"] = employee.pop("id", None)
        base.update(employee)
        return base


class TypedModel(models.Model):
    """models.Model but with better typehint support"""

    if TYPE_CHECKING:
        objects: models.Manager

    def as_json(self):
        base = {"id": self.pk}
        base.update(json.loads(serializers.serialize("json", (self,)))[0]["fields"])
        return base

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
    id: int = models.BigIntegerField(primary_key=True, unique=True)  # type: ignore
    tag = models.CharField(max_length=150)
    name = models.CharField(max_length=150)
    manufacture = models.CharField(max_length=150)
    pm_frequency = models.CharField(max_length=5, choices=Periodicity.choices, default=Periodicity.MONTHLY)
    work_place = models.ForeignKey(WorkPlace, on_delete=models.SET_NULL, blank=True, null=True)
    cost = models.IntegerField()
    picture = models.CharField(max_length=32, blank=True, default=generate_hexa_id)
    location = models.CharField(max_length=150)
    installation_date = models.DateField()
    warranty_date = models.DateField()
    arrival_date = models.DateField()
    note = models.CharField(max_length=150, blank=True)

    objects = EquipmentManager()

    def work_order_format(self) -> str:
        return f"{self.name} - {self.tag}"

    def __str__(self) -> str:
        return f"{self.name} ({self.tag})"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = snowflake()
        super().save(*args, **kwargs)


class Timer(TypedModel):
    name = models.SlugField(max_length=150)
    # repeat = -1 means it'll repeat forever
    repeat = models.IntegerField(default=0)  # type: ignore
    # if frequency is null or blank, it'll cancel out repeat's value, we'll assume that it only meant to execute once
    repeat_frequency = models.CharField(
        max_length=5, choices=Periodicity.choices, default=Periodicity.MONTHLY, blank=True, null=True
    )
    expires_at = models.DateTimeField()
    extra = models.JSONField(default=dict)

    objects = TimerManager()


class WorkOrder(TypedModel):
    type = models.CharField(max_length=5, choices=WorkOrderType.choices)
    code = models.IntegerField()  # will be generated automatically, last_row.code + 1
    description = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField()
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    is_complete = models.BooleanField(default=False)  # type: ignore

    objects = WorkOrderManager()

    class Meta:
        unique_together = ("type", "code")
