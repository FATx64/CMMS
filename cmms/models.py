from typing import TYPE_CHECKING

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from cmms.enums import UserType
from cmms.utils import handle_avatar_upload, snowflake


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

    def from_form(self, form_data: dict, **kwargs):
        u = self.create_user(
            form_data["email"],
            form_data.get("password", form_data.get("password2")),
            type=kwargs.get("type", UserType.ENGINEER),
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
            work_hour=form_data["work_hour"],
            work_place=form_data.get("work_place"),
            avatar=avatar or "",
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
    address = models.CharField(max_length=150, blank=True)
    work_hour = models.IntegerField()
    # Empty by default since on first-time setup Work Center is empty
    work_place = models.ForeignKey(WorkPlace, on_delete=models.CASCADE, blank=True, null=True, default=None)
    avatar = models.CharField(max_length=32, blank=True, default="")  # utils.generate_hexa_id()

    def full_name(self):
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
