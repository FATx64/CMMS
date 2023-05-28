from pathlib import Path
from django.http.response import HttpResponse
from django.shortcuts import redirect
from django.urls import include, path, re_path

from cmms import views


dashboard_urls = (
    [
        re_path('^/?$', lambda _: redirect("/dashboard/home"), name="index"),
        re_path('^/home/?$', views.DashboardView.as_view(), name="home"),
        re_path('^/users/?$', views.DashboardEmployeeView.as_view(), name="users"),
        re_path('^/workplace/?$', views.DashboardWorkPlaceView.as_view(), name="workplace"),
    ],
    "dashboard"
)


def avatars(request, user_id, file_id):
    path = Path("data/avatars") / user_id / file_id
    with open(path, "rb") as a:
       response = HttpResponse(a.read())
    response["Content-Type"] = ""
    response["Content-Disposition"] = "inline; filename=\"" + file_id + "\""
    return response


urlpatterns = [
    re_path("^$", views.HomeView.as_view(), name="index"),
    re_path(r"^avatars/(?P<user_id>\d+)/(?P<file_id>[\w]+)", avatars),
    re_path("^setup/?$", views.SetupView.as_view(), name="setup"),
    re_path("^dashboard", include(dashboard_urls), name="dashboard"),
    re_path("^logout/?$", views.logout_view, name="logout"),
    path("__reload__", include("django_browser_reload.urls"), name="meta_reload"),
]
