from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from cmms.decorators import admin_exists
from cmms.forms import SetupForm


@method_decorator(admin_exists, name="dispatch")
class HomeView(TemplateView):
    template_name = "home.html"


class SetupView(FormView):
    template_name = "setup.html"
    form_class = SetupForm
    success_url = "/"

    def form_valid(self, form: SetupForm):
        user = form.save()
        return HttpResponse(user.email)
