from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from cmms.decorators import admin_exists
from cmms.forms import SetupForm, LoginForm


@method_decorator(admin_exists, name="dispatch")
class HomeView(FormView):
    template_name = "home.html"
    form_class = LoginForm
    success_url = "/dashboard"

    def form_valid(self, form: LoginForm):
        return redirect(self.success_url)


class SetupView(FormView):
    template_name = "setup.html"
    form_class = SetupForm
    success_url = "/"

    def form_valid(self, form: SetupForm):
        form.save()
        return redirect(self.success_url)
