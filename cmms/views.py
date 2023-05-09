from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from cmms.decorators import admin_exists


@method_decorator(admin_exists, name="dispatch")
class HomeView(TemplateView):
    template_name = "home.html"


class SetupView(View):
    def get(self, request):
        return HttpResponse("Hello World")
