from __future__ import annotations

from django import forms
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from cmms.models import User


class SetupForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
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
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get("password2")
        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                self.add_error("password2", error)

    def save(self) -> User:
        return User.objects.create_superuser(self.cleaned_data["email"], self.cleaned_data["password2"])