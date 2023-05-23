from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from cmms.decorators import admin_exists, admin_not_exists
from cmms.forms import SetupForm, LoginForm


@method_decorator(admin_exists, name="dispatch")
class HomeView(FormView):
    template_name = "home.html"
    form_class = LoginForm
    success_url = "/dashboard"

    def get(self, request, *args, **kwargs):
        print(request.user.id)
        # TODO: Redirect user to dashboard when user is already logged in?
        return super().get(request, *args, **kwargs)

    def form_valid(self, form: LoginForm):
        user = form.authenticate()
        if user:
            login(self.request, user)
            rt = self.request.GET.get("next", self.success_url)
            return redirect(rt)
        else:
            # TODO: Handle failed auth
            pass


@method_decorator(admin_not_exists, name="dispatch")
class SetupView(FormView):
    template_name = "setup.html"
    form_class = SetupForm
    success_url = "/"

    def form_valid(self, form: SetupForm):
        user = form.save()
        if user:
            rt = self.request.GET.get("next", self.success_url)
            return redirect(rt)
        else:
            # TODO: Handle failed registration
            pass


@method_decorator(login_required(login_url="/"), name="dispatch")
class DashboardView(TemplateView):
    template_name = "dashboard/index.html"
