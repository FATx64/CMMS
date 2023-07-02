from __future__ import annotations

from typing import TYPE_CHECKING, Type

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.forms.forms import Form
from django.http.response import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView

from cmms import forms, models, utils
from cmms.decorators import admin_exists, admin_not_exists


if TYPE_CHECKING:
    from cmms.models import TypedModel


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


class CMMSJSONModelView(View):
    model: Type[TypedModel] | Type[models.User] | None = None

    def get(self, request, *args, **kwargs):
        if not self.model:
            raise RuntimeError

        pk = kwargs.get("id")
        if not pk:
            return super().get(request, *args, **kwargs)  # type: ignore
        return JsonResponse(self.model.objects.get(pk=pk).as_json())


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
class AJAXEmployeeView(CMMSJSONModelView):
    model = models.User


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
            work_place_id=getattr(user.employee.work_place, "id", None),
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
class AJAXWorkPlaceView(CMMSJSONModelView):
    model = models.WorkPlace


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardWorkPlaceView(CMMSFormView):
    template_name = "dashboard/workplace.html"
    form_class = forms.WorkPlaceForm
    form_classes = [forms.EditWorkPlaceForm]

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
        workplaces = [models.WorkPlace(pk=None, code=-1, name="No Work Center", location="The Void")]
        workplaces.extend(models.WorkPlace.objects.all().order_by("code"))
        context["workplaces"] = workplaces
        return context

    def form_valid(self, form: forms.WorkPlaceForm | forms.EditWorkPlaceForm):
        form.save()
        return redirect(self.request.path_info)


@method_decorator(login_required(login_url="/"), name="dispatch")
class AJAXEquipmentView(CMMSJSONModelView):
    model = models.Equipment


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardEquipmentView(CMMSFormView):
    template_name = "dashboard/equipment.html"
    form_class = forms.EquipmentForm
    form_classes = [forms.EditEquipmentForm]

    def post(self, request, *args, **kwargs):
        manage: str | None = request.POST.get("manage")
        if not manage:
            return super().post(request, *args, **kwargs)
        if manage.startswith("delete"):
            p = models.Equipment.objects.get(pk=manage.split(":")[1])
            if p:
                p.delete()
        return redirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workplaces_exists"] = len(models.WorkPlace.objects.all()) > 0
        context["equipments"] = models.Equipment.objects.all()
        return context

    def form_valid(self, form: forms.EquipmentForm | forms.EditEquipmentForm):
        form.save()
        return redirect(self.request.path_info)


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardWorkOrderView(CMMSFormView):
    template_name = "dashboard/workorder.html"
    form_class = forms.WorkOrderForm

    def post(self, request, *args, **kwargs):
        manage: str | None = request.POST.get("manage")
        if not manage:
            return super().post(request, *args, **kwargs)
        if manage.startswith("delete"):
            p = models.WorkOrder.objects.get(pk=manage.split(":")[1])
            if p:
                p.delete()
        return redirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        utils.export_workorder_to_xl()
        context = super().get_context_data(**kwargs)
        context["equipments_exists"] = len(models.Equipment.objects.all()) > 0
        context["workorders"] = models.WorkOrder.objects.all()
        return context

    def form_valid(self, form: forms.WorkOrderForm):
        form.save()
        return redirect(self.request.path_info)


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardAgentView(CMMSFormView):
    template_name = "dashboard/agent.html"
    form_class = forms.AgentForm
    form_classes = [forms.EditAgentForm]

    def post(self, request, *args, **kwargs):
        manage: str | None = request.POST.get("manage")
        if not manage:
            return super().post(request, *args, **kwargs)
        if manage.startswith("delete"):
            p = models.Agent.objects.get(pk=manage.split(":")[1])
            if p:
                p.delete()
        return redirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["agents"] = models.Agent.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return redirect(self.request.path_info)


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardSparepartView(CMMSFormView):
    template_name = "dashboard/sparepart.html"
    form_class = forms.SparepartForm
    form_classes = [forms.EditSparepartForm]

    def post(self, request, *args, **kwargs):
        manage: str | None = request.POST.get("manage")
        if not manage:
            return super().post(request, *args, **kwargs)
        if manage.startswith("delete"):
            p = models.Sparepart.objects.get(pk=manage.split(":")[1])
            if p:
                p.delete()
        return redirect(self.request.path_info)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["equipments_exists"] = len(models.Equipment.objects.all()) > 0
        context["spareparts"] = models.Sparepart.objects.all()
        return context

    def form_valid(self, form):
        form.save()
        return redirect(self.request.path_info)
