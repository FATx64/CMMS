from __future__ import annotations

from django import forms
from django.contrib.auth import authenticate, password_validation
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

from cmms.enums import UserType
from cmms.models import User, WorkPlace


class CMMSForm(forms.Form):
    form_id = ""

    @property
    def modal_id(self) -> str:
        return f"{self.form_id}-modal"

    template_name_div = "form/basic.html"

    def require_context(self, context=None):
        return context or self.get_context() or {}


class SetupForm(CMMSForm):
    id = forms.CharField(label="ID")  # Employee ID
    first_name = forms.CharField(label="First Name", max_length=150)
    last_name = forms.CharField(label="Last Name", max_length=150)
    address = forms.CharField(label="Address", max_length=150)
    phone_number = PhoneNumberField(label="Phone", region="ID")
    age = forms.DateField(label="Date of Birth", widget=forms.NumberInput(attrs={"type": "date"}))
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
        return authenticate(email=self.cleaned_data.get("email"), password=self.cleaned_data.get("password"))


class EmployeeForm(CMMSForm):
    form_id = "employee"

    id = forms.CharField(label="ID")  # Employee ID
    first_name = forms.CharField(label="First Name", max_length=150)
    last_name = forms.CharField(label="Last Name", max_length=150)
    address = forms.CharField(label="Address", max_length=150)
    phone_number = PhoneNumberField(label="Phone", region="ID")
    age = forms.DateField(label="Date of Birth", widget=forms.NumberInput(attrs={"type": "date"}))
    work_hour = forms.IntegerField(label="Work Hour")
    work_place = forms.ModelChoiceField(label="Work Center", queryset=WorkPlace.objects.all(), empty_label=None)
    avatar = forms.ImageField(
        label="Picture",
        widget=forms.FileInput(attrs={"class": "px-3"}),
        required=False,
    )
    email = forms.EmailField(label="Email Address", required=True)
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=True,
    )

    def save(self):
        return User.objects.from_form(self.cleaned_data)


class WorkPlaceForm(CMMSForm):
    form_id = "workplace"

    name = forms.CharField(label="Name")
    code = forms.IntegerField(label="Code")
    location = forms.CharField(label="Location")

    def save(self):
        workplace = WorkPlace(
            code=self.cleaned_data["code"], name=self.cleaned_data["name"], location=self.cleaned_data["location"]
        )
        workplace.save()
        return workplace
