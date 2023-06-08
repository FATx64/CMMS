from __future__ import annotations

from typing import Type

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.forms.forms import Form
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from cmms import forms, models
from cmms.decorators import admin_exists, admin_not_exists


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


@method_decorator(admin_exists, name="dispatch")
class HomeView(FormView):
    template_name = "home.html"
    form_class = forms.LoginForm
    success_url = "/dashboard"

    def get(self, request, *args, **kwargs):
        # TODO: Redirect user to dashboard when user is already logged in?
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: forms.LoginForm):
        user = form.authenticate()
        if user:
            login(self.request, user)
            rt = self.request.GET.get("next", self.success_url)
            return redirect(rt)
        else:
            # TODO: Handle failed auth
            return redirect(".")


@method_decorator(admin_not_exists, name="dispatch")
class SetupView(FormView):
    template_name = "setup.html"
    form_class = forms.SetupForm
    success_url = "/"

    def form_valid(self, form: forms.SetupForm):
        user = form.save()
        if user:
            rt = self.request.GET.get("next", self.success_url)
            return redirect(rt)
        else:
            # TODO: Handle failed registration
            return redirect(".")


@login_required(login_url="/")
def logout_view(request):
    logout(request)
    return redirect("/")


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard/index.html"


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardEmployeeView(CMMSFormView):
    template_name = "dashboard/users.html"
    form_class = forms.EmployeeForm
    form_classes = [forms.EditEmployeeForm]

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get("id")
        if not user_id:
            return super().get(request, *args, **kwargs)
        user = models.User.objects.get(pk=user_id)
        rt = dict(
            id=user.id,
            employee_id=user.employee.employee_id,
            first_name=user.employee.first_name,
            last_name=user.employee.last_name,
            phone_number=str(user.employee.phone_number),
            date_of_birth=user.employee.date_of_birth,
            address=user.employee.address,
            work_hour=user.employee.work_hour,
            work_place_id=user.employee.work_place.id,
            avatar=user.employee.avatar,
        )
        return JsonResponse(rt)

    def post(self, request, *args, **kwargs):
        manage: str | None = request.POST.get("manage")
        if not manage:
            return super().post(request, *args, **kwargs)
        if manage.startswith("delete"):
            p = models.User.objects.get(pk=manage.split(":")[1])
            if p:
                p.delete()
        return redirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {"workplaces_exists": len(models.WorkPlace.objects.all()) > 0, "employees": models.Employee.objects.all()}
        context.update(data)
        return context

    def form_valid(self, form: forms.EmployeeForm):
        form.save()
        return redirect(self.request.path_info)


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardWorkPlaceView(CMMSFormView):
    template_name = "dashboard/workplace.html"
    form_class = forms.WorkPlaceForm
    form_classes = [forms.EditWorkPlaceForm]

    def get(self, request, *args, **kwargs):
        wp_id = kwargs.get("id")
        if not wp_id:
            return super().get(request, *args, **kwargs)
        work_place = models.WorkPlace.objects.get(pk=wp_id)
        rt = dict(
            id=work_place.id,
            name=work_place.name,
            code=work_place.code,
            location=work_place.location,
        )
        return JsonResponse(rt)

    def post(self, request, *args, **kwargs):
        manage: str | None = request.POST.get("manage")
        if not manage:
            return super().post(request, *args, **kwargs)
        if manage.startswith("delete"):
            p = models.WorkPlace.objects.get(pk=manage.split(":")[1])
            if p:
                p.delete()
        return redirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workplaces"] = models.WorkPlace.objects.all()
        return context

    def form_valid(self, form: forms.WorkPlaceForm | forms.EditWorkPlaceForm):
        form.save()
        return redirect(self.request.path_info)
