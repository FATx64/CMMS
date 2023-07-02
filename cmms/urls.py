import sys
from pathlib import Path

from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import include, path, re_path
from graphene_django.views import GraphQLView

from cmms import views
from cmms.timer import Timer


api_urls = (
    [
        re_path(r'^/?$', lambda _: redirect("/dashboard/home", name="index")),
        re_path(r'^/equipment/(?P<id>[\w]+)/?$', views.AJAXEquipmentView.as_view(), name="ajax_equipment"),
        re_path(r'^/users/(?P<id>[\w]+)/?$', views.AJAXEmployeeView.as_view(), name="ajax_users"),
        re_path(r'^/workplace/(?P<id>[\w]+)/?$', views.AJAXWorkPlaceView.as_view(), name="ajax_workplace"),
    ],
    "api",
)

dashboard_urls = (
    [
        re_path(r'^/?$', lambda _: redirect("/dashboard/home"), name="index"),
        re_path(r'^/home/?$', views.DashboardView.as_view(), name="home"),
        re_path(r'^/users/?$', views.DashboardEmployeeView.as_view(), name="users"),
        re_path(r'^/workplace/?$', views.DashboardWorkPlaceView.as_view(), name="workplace"),
        re_path(r'^/equipment/?$', views.DashboardEquipmentView.as_view(), name="equipment"),
        re_path(r'^/workorder/?$', views.DashboardWorkOrderView.as_view(), name="workorder"),
        re_path(r'^/agent/?$', views.DashboardAgentView.as_view(), name="agent"),
    ],
    "dashboard",
)


def image(_path: Path):
    def predicate(request, user_id, file_id):
        path = _path / user_id / file_id
        with open(path, "rb") as a:
            response = HttpResponse(a.read())
        response["Content-Type"] = ""
        response["Content-Disposition"] = "inline; filename=\"" + file_id + "\""
        return response

    return predicate


urlpatterns = [
    re_path("^$", views.HomeView.as_view(), name="index"),
    re_path(r"^avatars/(?P<user_id>\d+)/(?P<file_id>[\w]+\.webp)", image(Path("data/avatars"))),
    re_path(r"^pictures/(?P<user_id>\d+)/(?P<file_id>[\w]+\.webp)", image(Path("data/pictures"))),
    re_path("^setup/?$", views.SetupView.as_view(), name="setup"),
    re_path("^dashboard", include(dashboard_urls), name="dashboard"),
    re_path("^api/v1", include(api_urls), name="api"),
    re_path("^graphql/?$", GraphQLView.as_view(graphiql=True)),
    re_path("^logout/?$", views.logout_view, name="logout"),
    path("__reload__", include("django_browser_reload.urls"), name="meta_reload"),
]


if "runserver" in sys.argv:
    Timer().start()
