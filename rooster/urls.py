from django.conf.urls import url
from django.urls import path, include

from profile.views import DashboardView, SettingsView

urlpatterns = [
    url("", include("social_django.urls", namespace="social")),
    url(r"^tz_detect/", include("tz_detect.urls")),
    path("", DashboardView.as_view(), name="dashboard"),
    path("settings", SettingsView.as_view(), name="settings"),
]
