from __future__ import annotations

from typing import TYPE_CHECKING, Any, Type

from django.forms.forms import Form
from django.http import HttpRequest
from django.http.response import JsonResponse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import FormView

from cmms import forms
from cmms.core import models


if TYPE_CHECKING:
    from cmms.core.models import TypedModel


# TODO: Use this
class CMMSTemplateResponseMixin(TemplateResponseMixin):
    if TYPE_CHECKING:
        request: Any

    template_partial_name: str | None = None

    def render_to_response(self, context, **response_kwargs):
        if not self.request.htmx:
            return super().render_to_response(context, **response_kwargs)

        # TODO: Return partial
        return super().render_to_response(context, **response_kwargs)


class CMMSFormView(FormView):
    """FormView with multi-form support. form_class will act as default form"""

    form_classes: list[Type[forms.CMMSForm]] = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for form in self.form_classes:
            _id = form.Meta.id
            form = form
            self.Meta.forms[_id] = form

    def get_cmms_form(self, id: str):
        return self.get_form(self.Meta.forms.get(id))

    def post(self, request, *args, **kwargs):
        """Directly copied from Django's source code and modified to allow multi-form support

        REF: https://github.com/django/django/blob/0030814/django/views/generic/edit.py#L144-L153
        """
        form = self.get_cmms_form(request.POST.get("form_id"))
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        initialized = {}
        for k, v in self.Meta.forms.items():
            _id = k
            form = self.get_form(v)
            initialized[_id] = form

        ctx.update({"forms": self.Meta.forms})
        return ctx

    class Meta:
        forms: dict[str, Type[Form]] = {}


# TODO: Deprecated, delete later. Use GraphQL instead
class CMMSJSONModelView(View):
    model: Type[TypedModel] | Type[models.User] | None = None

    def get(self, request, *args, **kwargs):
        if not self.model:
            raise RuntimeError

        pk = kwargs.get("id")
        if not pk:
            return super().get(request, *args, **kwargs)  # type: ignore
        return JsonResponse(self.model.objects.get(pk=pk).as_json())
