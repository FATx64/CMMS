"""cmms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.shortcuts import redirect
from django.urls import include, path, re_path

from cmms.views import DashboardEmployeeView, DashboardView, HomeView, SetupView


dashboard_urls = (
    [
        re_path('^$', lambda _: redirect("/dashboard/home"), name="index"),
        re_path('^/home/?$', DashboardView.as_view(), name="home"),
        re_path('^/users/?$', DashboardEmployeeView.as_view(), name="users"),
    ],
    "dashboard"
)


urlpatterns = [
    re_path("^$", HomeView.as_view(), name="index"),
    re_path("^setup/?$", SetupView.as_view(), name="setup"),
    re_path("^dashboard", include(dashboard_urls), name="dashboard"),
    path("__reload__", include("django_browser_reload.urls"), name="meta_reload"),
]
