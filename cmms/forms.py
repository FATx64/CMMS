from __future__ import annotations

from typing import Type

from django import forms
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from cmms.enums import Periodicity, UserType, WorkOrderType
from cmms.models import Equipment, User, WorkOrder, WorkPlace
from cmms.utils import JS, handle_avatar_upload


class CMMSDateField(forms.DateField):
    def __init__(self, *, input_formats=None, **kwargs):
        kwargs.setdefault("widget", forms.NumberInput(attrs={"type": "date"}))
        super().__init__(input_formats=input_formats, **kwargs)


class CMMSForm(forms.Form):
    @property
    def meta(self) -> Type[Meta]:
        return self.Meta

    @property
    def modal_id(self) -> str:
        return f"{self.Meta.id}-modal"

    template_name_div = "form/basic.html"

    def get_context(self) -> dict | None:
        rt = super().get_context()
        rt.update({"meta": self.meta})
        return rt

    def require_context(self, context=None):
        return context or self.get_context() or {}

    class Meta:
        id = "form"


class SetupForm(CMMSForm):
    id = forms.CharField(label="ID")  # Employee ID
    first_name = forms.CharField(label="First Name", max_length=150)
    last_name = forms.CharField(label="Last Name", max_length=150)
    address = forms.CharField(label="Address", max_length=150)
    phone_number = PhoneNumberField(label="Phone", region="ID")
    date_of_birth = CMMSDateField(label="Date of Birth")
    work_hour = forms.IntegerField(label="Work Hour")
    avatar = forms.ImageField(
        label="Picture",
        widget=forms.FileInput(attrs={"class": "px-3"}),
        required=False,
    )
    email = forms.EmailField(label="Email Address", required=True)
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=True,
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=True,
    )

    def clean_password2(self) -> str | None:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                "The two password fields didn’t match",
                code="password_mismatch",
            )
        return password2

    def _post_clean(self) -> None:
        super()._post_clean()
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                self.add_error("password1", error)
                self.add_error("password2", error)
        else:
            raise RuntimeError("How?")

    def save(self) -> User:
        return User.objects.from_form(self.cleaned_data, type=UserType.ADMIN)


class LoginForm(CMMSForm):
    email = forms.EmailField(label="Email address")
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )

    def _post_clean(self) -> None:
        super()._post_clean()
        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                self.add_error("password", error)

    def authenticate(self):
        return authenticate(**self.cleaned_data)


class EmployeeCommon(CMMSForm):
    employee_id = forms.CharField(label="ID")  # Employee ID
    first_name = forms.CharField(label="First Name", max_length=150)
    last_name = forms.CharField(label="Last Name", max_length=150)
    address = forms.CharField(label="Address", max_length=150)
    phone_number = PhoneNumberField(label="Phone", region="ID")
    date_of_birth = CMMSDateField(label="Date of Birth")
    work_hour = forms.IntegerField(label="Work Hour")
    work_place = forms.ModelChoiceField(label="Work Center", queryset=WorkPlace.objects.all(), empty_label=None)  # type: ignore
    avatar = forms.ImageField(
        label="Picture",
        widget=forms.FileInput(attrs={"class": "px-3"}),
    )

    def save(self):
        raise NotImplementedError()


class EmployeeForm(EmployeeCommon):
    email = forms.EmailField(label="Email Address", required=True)
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=True,
    )
    type = forms.ChoiceField(label="Account Type", choices=UserType.choices)

    def _post_clean(self) -> None:
        super()._post_clean()
        password = self.cleaned_data.get("password")
        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                self.add_error("password", error)

    def save(self):
        return User.objects.from_form(self.cleaned_data)

    class Meta:
        id = "new_employee"


class EditEmployeeForm(EmployeeCommon):
    id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar"].required = False

    def save(self):
        user = User.objects.get(pk=self.cleaned_data.pop("id"))
        employee = user.employee

        avatar = self.cleaned_data.pop("avatar", None)
        if avatar:
            employee.avatar = handle_avatar_upload(user.id, avatar)

        for key, value in self.cleaned_data.items():
            setattr(employee, key, value)

        employee.save()
        return employee

    @property
    def media(self):
        return forms.Media(
            js=[
                JS("js/edit_employee.js", {"data-id": self.meta.id}),
            ]
        )

    class Meta:
        id = "edit_employee"


class WorkPlaceCommon(CMMSForm):
    name = forms.CharField(label="Name")
    code = forms.IntegerField(label="Code")
    location = forms.CharField(label="Location")

    def save(self):
        raise NotImplementedError()


class WorkPlaceForm(WorkPlaceCommon):
    def save(self):
        workplace = WorkPlace(**self.cleaned_data)
        workplace.save()
        return workplace

    class Meta:
        id = "new_workplace"


class EditWorkPlaceForm(WorkPlaceCommon):
    id = forms.IntegerField(widget=forms.HiddenInput())

    def save(self):
        return WorkPlace.objects.filter(pk=self.cleaned_data.pop("id")).update(**self.cleaned_data)

    @property
    def media(self):
        return forms.Media(
            js=[
                JS("js/edit_workplace.js", {"data-id": self.meta.id}),
            ]
        )

    class Meta:
        id = "edit_workplace"


class EquipmentCommon(CMMSForm):
    tag = forms.CharField(max_length=150)
    name = forms.CharField(max_length=150)
    manufacture = forms.CharField(max_length=150)
    pm_frequency = forms.ChoiceField(label="PM", choices=Periodicity.choices)
    work_place = forms.ModelChoiceField(label="Work Station", queryset=WorkPlace.objects.all(), empty_label=None)  # type: ignore
    cost = forms.IntegerField()
    picture = forms.ImageField(
        label="Picture",
        widget=forms.FileInput(attrs={"class": "px-3"}),
    )
    location = forms.CharField(max_length=150)
    installation_date = CMMSDateField()
    warranty_date = CMMSDateField()
    arrival_date = CMMSDateField()
    note = forms.CharField(max_length=150, required=False)


class EquipmentForm(EquipmentCommon):
    def save(self):
        return Equipment.objects.create(**self.cleaned_data)

    class Meta:
        id = "new_equipment"


class EditEquipmentForm(EquipmentCommon):
    id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["picture"].required = False

    def save(self):
        return Equipment.objects.edit(**self.cleaned_data)

    @property
    def media(self):
        return forms.Media(
            js=[
                JS("js/edit_equipment.js", {"data-id": self.meta.id}),
            ]
        )

    class Meta:
        id = "edit_equipment"


class WorkOrderCommon(CMMSForm):
    type = forms.ChoiceField(choices=WorkOrderType.choices)
    description = forms.CharField(max_length=150)
    start_date = CMMSDateField()
    end_date = CMMSDateField()
    equipment = forms.ModelChoiceField(queryset=Equipment.objects.all(), empty_label=None)  # type: ignore


class WorkOrderForm(WorkOrderCommon):
    def save(self):
        return WorkOrder.objects.create(**self.cleaned_data)

    class Meta:
        id = "new_workorder"
