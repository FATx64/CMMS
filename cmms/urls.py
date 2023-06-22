from pathlib import Path

from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import include, path, re_path

from cmms.timer import Timer
from cmms import events, views


dashboard_urls = (
    [
        re_path(r'^/?$', lambda _: redirect("/dashboard/home"), name="index"),
        re_path(r'^/home/?$', views.DashboardView.as_view(), name="home"),
        re_path(r'^/users/?$', views.DashboardEmployeeView.as_view(), name="users"),
        re_path(r'^/users/(?P<id>[\w]+)/?$', views.DashboardEmployeeView.as_view(), name="ajax_users"),
        re_path(r'^/workplace/?$', views.DashboardWorkPlaceView.as_view(), name="workplace"),
        re_path(r'^/workplace/(?P<id>[\w]+)/?$', views.DashboardWorkPlaceView.as_view(), name="ajax_workplace"),
        re_path(r'^/equipment/?$', views.DashboardEquipmentView.as_view(), name="equipment"),
        re_path(r'^/workorder/?$', views.DashboardWorkOrderView.as_view(), name="workorder"),
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
    re_path("^logout/?$", views.logout_view, name="logout"),
    path("__reload__", include("django_browser_reload.urls"), name="meta_reload"),
]


events = events.Events()
timer = Timer()
timer.start()
