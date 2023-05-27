from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from cmms.decorators import admin_exists, admin_not_exists
from cmms import forms, models


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


def logout_view(request):
    logout(request)
    return redirect("/")


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard/index.html"


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardEmployeeView(FormView):
    template_name = "dashboard/users.html"
    form_class = forms.EmployeeForm


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardWorkPlaceView(FormView):
    template_name = "dashboard/workplace.html"
    form_class = forms.WorkPlaceForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["workplaces"] = models.WorkPlace.objects.all()
        return context

    def form_valid(self, form: forms.WorkPlaceForm):
        form.save()
        return redirect(self.request.path_info)
